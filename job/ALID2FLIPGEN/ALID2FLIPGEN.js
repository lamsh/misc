/****************************************************************************
 \file      ALID2FLIPGEN.js
 \author    SENOO, Ken
 \copyright CC0
 \date      created date: 2016-01-29T16:31+09:00
 \date      updated date: 2016-02-18T13:24+09:00
 ****************************************************************************/

/**
 \brief AFIMEX�̃��b�V����FLIPGEN�œǂݍ��߂郁�b�V���ɂ���
 �g����
 1. AFIMEX�Łm�t�@�C���n���m���f�����n�A�m���b�V�������n�^�u���m�c�[���n���m���b�V���̃t�@�C���o�́n��*.msh�ŕۑ��B
 2. ���́mALID2FLIPGEN.js�n�v���O������ۑ�����.msh�t�@�C���Ɠ����ꏊ�ɒu���B
 3. ���́mALID2FLIPGEN.js�n�v���O�������_�u���N���b�N���邩.msh�t�@�C�������̃v���O�����Ƀh���b�O�h���b�v����B
 4. �����f�B���N�g���Ɋg���q��.d�ƂȂ����t�@�C�������������B
 ��Fmesh.msh -> mesh.d
*/

/**
 �쐬�|�C���g
 * �O�p�`�v�f�͓����ߓ_��ǉ����Ė������l�p�`�v�f�ɂ���B
 * �`���ɐߓ_�����A�v�f�������L��
 * ���̒���
 * �ߓ_�ɐ��`��ԗp�ԍ��̕t�^
 * �v�f�ɍޗ��ԍ��̕t�^
*/

/// ECMAScript6��startsWith�̎���
if (!String.prototype.startsWith) {
  String.prototype.startsWith = function(searchString, position) {
    position = position || 0;
    return this.lastIndexOf(searchString, position) === position;
  };
}

/// �������p�֐�
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

//�@�h���b�O�h���b�v�Ή�
var arg = WScript.Arguments;

// �������Ȃ����*.msh�������ɂ���
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

  // ����
  var fs = fso.OpenTextFile(fpath);
  var text = fs.ReadAll().split(/\r\n|\r|\n/);
  fs.Close();

  // AFIMEX��ALID�̏o�̓��b�V���łȂ���Ζ���
  if (!text[0].startsWith("NODE")){
    continue
  }

  // ���ߓ_���Ƒ��v�f�����擾
  var total_element = text.slice(-1)[0].split(/\s+/)[0];
  for (var i = 0; i < text.length; ++i) {
    if (text[i].startsWith("ELEM")) {
      var total_node = text[i-1].split(/\s+/)[0];
      break;
    }
  }

  // �o�͗p�f�[�^�̗p��
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

    // �O�p�`�v�f���l�p�`�v�f�Ɠ����ɂ��鏈��
    if (elem.length !== 6) {
      line = line + padding(elem.slice(-1)[0], " ", 5);
    }
    mesh.push(line);
  }

  // �o��
  fpath = fso.GetParentFolderName(fpath) + "\\" + fso.GetBaseName(fpath) + ".d";

  var fs = fso.CreateTextFile(fpath, true);
  fs.Write(mesh.join("\n"));
  fs.Close();
}
