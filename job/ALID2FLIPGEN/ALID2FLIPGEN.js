/****************************************************************************
 \file      ALID2FLIPGEN.js
 \author    SENOO, Ken
 \copyright CC0
 \date      created date: 2016-01-29T16:31+09:00
 \date      updated date: 2016-02-18T13:24+09:00
 ****************************************************************************/

/**
 \brief AFIMEXのメッシュをFLIPGENで読み込めるメッシュにする
 使い方
 1. AFIMEXで［ファイル］＞［モデル化］、［メッシュ分割］タブ＞［ツール］＞［メッシュのファイル出力］で*.mshで保存。
 2. この［ALID2FLIPGEN.js］プログラムを保存した.mshファイルと同じ場所に置く。
 3. この［ALID2FLIPGEN.js］プログラムをダブルクリックするか.mshファイルをこのプログラムにドラッグドロップする。
 4. 同じディレクトリに拡張子が.dとなったファイルが生成される。
 例：mesh.msh -> mesh.d
*/

/**
 作成ポイント
 * 三角形要素は同じ節点を追加して無理やり四角形要素にする。
 * 冒頭に節点総数、要素総数を記載
 * 桁の調整
 * 節点に線形補間用番号の付与
 * 要素に材料番号の付与
*/

/// ECMAScript6のstartsWithの実装
if (!String.prototype.startsWith) {
  String.prototype.startsWith = function(searchString, position) {
    position = position || 0;
    return this.lastIndexOf(searchString, position) === position;
  };
}

/// 桁調整用関数
function padding(str, chr, digit) {
  if (String(str).length >= digit){
    return str;
  }
  while (String(chr+str).length < digit) {
    chr += String(chr);
  }
  return String(chr+str).slice(-digit);
}

var fso = new ActiveXObject("Scripting.FileSystemObject");
var cwd = fso.GetAbsolutePathName("");

//　ドラッグドロップ対応
var arg = WScript.Arguments;

// 引数がなければ*.mshを引数にする
var args = new Array();
if (arg.length) {
  for (var i=0; i<arg.length; ++i){
    args.push(arg(i));
  }
}else {
  var files = fso.GetFolder(cwd).Files;
  var e = new Enumerator(files);
  for (; !e.atEnd(); e.moveNext()){
    var file = e.item();
    if (fso.GetExtensionName(file.Path) === "msh") {
      args.push(file.Path);
    }
  }
}

for (var i = 0; i < args.length; ++i){
  fpath = args[i];

  // 入力
  var fs = fso.OpenTextFile(fpath);
  var text = fs.ReadAll().split(/\r\n|\r|\n/);
  fs.Close();

  // AFIMEXのALIDの出力メッシュでなければ無視
  if (!text[0].startsWith("NODE")){
    continue
  }

  // 総節点数と総要素数を取得
  var total_element = text.slice(-1)[0].split(/\s+/)[0];
  for (var i = 0; i < text.length; ++i) {
    if (text[i].startsWith("ELEM")) {
      var total_node = text[i-1].split(/\s+/)[0];
      break;
    }
  }

  // 出力用データの用意
  var mesh = ["FEAP"];
  mesh.push(padding(total_node, " ", 5)+padding(total_element, " ", 5)+"    1");
  mesh.push("");

  mesh.push("COOR");
  for (var i = 0; !text[i].startsWith("ELEM"); ++i) {
    var line = text[i].slice(5);
    var line = line.slice(0,5) + "    0" + line.slice(10);
    mesh.push(line);
  }
  mesh.push("");

  mesh.push("ELEM");
  var elem_start_i;
  for (var i = 0; i < text.length; ++i) {
    if (text[i].startsWith("ELEM")) {
      elem_start_i = i;
      break;
    }
  }
  for (var i = elem_start_i; i < text.length; ++i) {
    var line = text[i].slice(5);
    var line = line.slice(0,5) + "    1" + line.slice(10);
    var elem = line.split(/\s+/);

    // 三角形要素を四角形要素と同じにする処理
    if (elem.length !== 6) {
      line = line + padding(elem.slice(-1)[0], " ", 5);
    }
    mesh.push(line);
  }

  // 出力
  fpath = fso.GetParentFolderName(fpath) + "\\" + fso.GetBaseName(fpath) + ".d";

  var fs = fso.CreateTextFile(fpath, true);
  fs.Write(mesh.join("\n"));
  fs.Close();
}
