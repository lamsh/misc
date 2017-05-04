/****************************************************************************
 \file      last_step_extract_ES_output.js
 \author    SENOO, Ken
 \copyright CC0
 \date      created date: 2015-12-14T21:46+09:00
 \date      updated date: 2016-02-16T17:43+09:00
 ****************************************************************************/

/**
 E.Sの計算結果をCSVで出力したものから、要素ごとにN、SYP、MZPの最大絶対値をCSVで抽出する。

 ## 使い方
 E.Sの計算結果をCSVで出力したファイルをこのプログラム（extract_es_output.js）にドラッグドロップするか、ダブルクリックで実行する。
 ダブルクリックで実行した場合、同じディレクトリのファイル内容の1行目が"Engineer's Studio Result"で始まるCSVファイルを処理する。

 ## 入出力
 入力：E.S.の計算結果をCSVで出力したファイル（ファイルの1行目が"Engineer's Studio Result"）
 出力：入力ファイル名-output.csv

 ## 処理のロジック
 CSVの下の方で2列目がElementのところから抽出を始める。
 必要な値：
 * MZP
 * N
 * SYP

 ありがたいことにMax ValueとMin Valueがフィールドに値が出力されているのでこれらを収集する。

 Max ValueとMin Valueを比較して絶対値が大きい方を採用。

 出力のイメージ
output.csv
,,最大絶対値,
要素名,N,SYP,MZP
躯体-001,1,1,1
躯体-001,2,2,2
*/

function get_abs_max(arg1, arg2){
  if (Math.abs(arg1) > Math.abs(arg2)){
    return arg1;
  } else {
    return arg2;
  }
}

var fso = new ActiveXObject("Scripting.FileSystemObject");
var cwd = fso.GetAbsolutePathName("");

// ドラッグドロップ対応
// 引数がなければ*.csvを引数にする
var arg = WScript.Arguments;
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
    if (fso.GetExtensionName(file.Path) === "csv") {
      args.push(file.Path);
    }
  }
}

var outtext = [",最終ステップ値,,,,端点種別,,最大絶対値,,,,端点種別,,ステップ数",
              "要素名,N,SYP,MZP,ABS(SYP),SYP,MZP,N,SYP,MZP,ABS(SYP),SYP,MZP,N,SYP,MZP"];

var node        = {N: 0, SYP: 0, MZP: 0};
var node_last   = {N: 0, SYP: 0, MZP: 0};
var i_node      = {N: 0, SYP: 0, MZP: 0};
var i_node_max  = {N: 0, SYP: 0, MZP: 0};
var i_node_min  = {N: 0, SYP: 0, MZP: 0};
var i_node_last = {N: 0, SYP: 0, MZP: 0};
var j_node      = {N: 0, SYP: 0, MZP: 0};
var j_node_max  = {N: 0, SYP: 0, MZP: 0};
var j_node_min  = {N: 0, SYP: 0, MZP: 0};
var j_node_last = {N: 0, SYP: 0, MZP: 0};

var step        = {N: 0, SYP: 0, MZP: 0};
var i_step      = {N: 0, SYP: 0, MZP: 0};
var i_step_max  = {N: 0, SYP: 0, MZP: 0};
var i_step_min  = {N: 0, SYP: 0, MZP: 0};
var j_step      = {N: 0, SYP: 0, MZP: 0};
var j_step_max  = {N: 0, SYP: 0, MZP: 0};
var j_step_min  = {N: 0, SYP: 0, MZP: 0};

var node_type      = {N: 0, SYP: 0, MZP: 0};
var node_last_type = {N: 0, SYP: 0, MZP: 0};

for (var i = 0; i < args.length; ++i) {
  fpath = args[i];

  var fs = fso.OpenTextFile(fpath);
  var text = fs.ReadAll().split(/\r\n|\r|\n/);
  fs.Close();

  // ESの結果でなければ無視
  if (text[0] !== "Engineer's Studio Result") {
    continue
  }

  // Elementが登場するまで配列を削除
  for (var i = 0; text[i].search(/Element/) === -1; ++i){}
  text.splice(0, i);

  // 最大ステップ数の取得
  for (var i = 0; text[i].search(/Max Value/) === -1; ++i) {}
  var step_last = text[i-1].split(",")[4];
  re_step = new RegExp(",,,," + step_last + ",");

  var is_i_node = true;
  for (var i = 0; i < text.length; ++i){
    // 収束結果は不要なので、収束結果のセクションが登場したら終了。
    if (text[i].search(/Non-Convergence/) !== -1){break;}

    var line = text[i];
    var is_last_step = line.search(re_step) !== -1;
    var is_max = line.search(/Max Value/) !== -1;
    var is_min = line.search(/Min Value/) !== -1;
    var is_max_step = line.search(/Max Step/) !== -1;
    var is_min_step = line.search(/Min Step/) !== -1;

    if (line.search(/Element/) !== -1){
      var element_name = line.split(",").pop();
    }

    var value = line.split(",");
    if (is_i_node){
      if (is_last_step){
        i_node_last.N   = value[5];
        i_node_last.SYP = value[6];
        i_node_last.MZP = value[10];
      } else if (is_max){
        i_node_max.N   = value[5];
        i_node_max.SYP = value[6];
        i_node_max.MZP = value[10];
      } else if (is_min){
        i_node_min.N   = value[5];
        i_node_min.SYP = value[6];
        i_node_min.MZP = value[10];
      } else if (is_max_step){
        i_step_max.N   = value[5];
        i_step_max.SYP = value[6];
        i_step_max.MZP = value[10];
      } else if (is_min_step){
        i_step_min.N   = value[5];
        i_step_min.SYP = value[6];
        i_step_min.MZP = value[10];

        is_i_node = false;
      }
    } else {
      if (is_last_step){
        j_node_last.N   = value[5];
        j_node_last.SYP = value[6];
        j_node_last.MZP = value[10];
      } else if (is_max){
        j_node_max.N   = value[5];
        j_node_max.SYP = value[6];
        j_node_max.MZP = value[10];
      } else if (is_min){
        j_node_min.N   = value[5];
        j_node_min.SYP = value[6];
        j_node_min.MZP = value[10];
      } else if (is_max_step){
        j_step_max.N   = value[5];
        j_step_max.SYP = value[6];
        j_step_max.MZP = value[10];
      } else if (is_min_step){
        j_step_min.N   = value[5];
        j_step_min.SYP = value[6];
        j_step_min.MZP = value[10];

        is_i_node = true;

        // このタイミングで絶対値を算出して出力用変数に値を追加
        i_node.N   = get_abs_max(i_node_max.N  , i_node_min.N  );
        i_node.SYP = get_abs_max(i_node_max.SYP, i_node_min.SYP);
        i_node.MZP = get_abs_max(i_node_max.MZP, i_node_min.MZP);

        j_node.N   = get_abs_max(j_node_max.N  , j_node_min.N  );
        j_node.SYP = get_abs_max(j_node_max.SYP, j_node_min.SYP);
        j_node.MZP = get_abs_max(j_node_max.MZP, j_node_min.MZP);

        i_step.N = (i_node.N === i_node_max.N) ? i_step_max.N : i_step_min.N;
        i_step.SYP = (i_node.SYP === i_node_max.SYP) ? i_step_max.SYP : i_step_min.SYP;
        i_step.MZP = (i_node.MZP === i_node_max.MZP) ? i_step_max.MZP : i_step_min.MZP;

        j_step.N = (j_node.N === j_node_max.N) ? j_step_max.N : j_step_min.N;
        j_step.SYP = (j_node.SYP === j_node_max.SYP) ? j_step_max.SYP : j_step_min.SYP;
        j_step.MZP = (j_node.MZP === j_node_max.MZP) ? j_step_max.MZP : j_step_min.MZP;

        // SYPはどちらかの絶対値の最大値
        node.SYP   = get_abs_max(i_node.SYP, j_node.SYP);
        node_type.SYP = (node.SYP === i_node.SYP) ? "i" : "j";
        // NはMZPの最大絶対値の位置での値
        if (Math.abs(i_node.MZP) > Math.abs(j_node.MZP)){
          node.MZP = i_node.MZP;
          node.N   = i_node.N;
          node_type.MZP = "i";
        } else {
          node.MZP = j_node.MZP;
          node.N   = j_node.N;
          node_type.MZP = "j";
        }
        step.N   = (node.N   === i_node.N)   ? i_step.N   : j_step.N;
        step.SYP = (node.SYP === i_node.SYP) ? i_step.SYP : j_step.SYP;
        step.MZP = (node.MZP === i_node.MZP) ? i_step.MZP : j_step.MZP;

        // SYPはどちらかの絶対値の最大値
        node_last.SYP = get_abs_max(i_node_last.SYP, j_node_last.SYP);
        node_last_type.SYP = (node.SYP === i_node.SYP) ? "i" : "j";
        // NはMZPの最大絶対値の位置での値
        if (Math.abs(i_node_last.MZP) > Math.abs(j_node_last.MZP)){
          node_last.MZP = i_node_last.MZP;
          node_last.N   = i_node_last.N;
          node_last_type.MZP = "i";
        } else {
          node_last.MZP = j_node_last.MZP;
          node_last.N   = j_node_last.N;
          node_last_type.MZP = "j";
        }

        outtext.push(element_name + "," +
            node_last.N + "," + node_last.SYP + "," + node_last.MZP + "," +
            Math.abs(node_last.SYP) + "," + node_last_type.SYP + "," +node_last_type.MZP + "," +
            node.N + "," + node.SYP + "," + node.MZP + "," +
            Math.abs(node.SYP) + "," + node_type.SYP + "," + node_type.MZP + "," +
            step.N + "," + step.SYP + "," +step.MZP);
      }
    }
  }

  fpath = fso.GetParentFolderName(fpath) + "\\" + fso.GetBaseName(fpath) + "-output.csv"
  try {
    var fs = fso.CreateTextFile(fpath, true);
    fs.Write(outtext.join("\n"));
  }catch (e){
    WScript.Echo(fpath + "ファイルに書き込めません。");
  }finally {
    fs.close();
  }
}
