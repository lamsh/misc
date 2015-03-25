' (File name: MyExcelVBA.bas)
' Author: SENOO, Ken
' LICENSE: CC0

Option Explicit


Sub AddNewSheet(sheet_name as String)
    ' �V�[�g������΍폜���āA�V�K�쐬�B
    Dim ws
    For Each ws In Worksheets
        If ws.Name = sheet_name Then
            Application.DisplayAlerts = False
            ws.Delete
            Application.DisplayAlerts = True
        End If
    Next ws

    ' �E�ׂɐV�K�V�[�g��ǉ��B
    Sheets.Add(After:=ActiveSheet).Name = sheet_name
End Sub


'' VBA�ł̓T�C�Y�̒P�ʂ�pt�B����pt�͈ȉ��̑Ή��ƂȂ��Ă���
'' 72 pt = 25.4 mm

'' Application.CentimetersToPoints�Ɠ���
Function cm2pt(cm as Double) as Double
    cm2pt = 72/25.4 * 10 * cm
End Function

'' Application.InchesToPoints�Ɠ���
Function pt2cm(pt as Double) as Double
    pt2cm = 0.1 * 25.4 / 72 * pt
End Function


'' �N���b�v�{�[�h�̓��e�𓯂��ꏊ��metafile.emf�ɕۑ�
''' TODO: Chart.CopyPicture�Œ��ڕۑ��ł��Ȃ��B���ƂŃR�s�[���Ȃ��ƃt�@�C���ɕۑ��ł��Ȃ��B
''' �����̃O���t��I������Ƌ�`�̈�ł܂Ƃ߂ĕۑ��ł���B

''' Original: http://www4.ocn.ne.jp/~outfocus/emf/emf.html

Private Type GUID
Data1 As Long
Data2 As Integer
Data3 As Integer
Data4(0 To 7) As Byte
End Type
Private Type PICTDESC
cbSizeofstruct As Long
picType As Long
hemf As Long
Padding(0 To 1) As Long
End Type
Const PICTYPE_ENHMETAFILE = 4

Private Declare PtrSafe Function OleCreatePictureIndirect Lib "olepro32.dll" (lpPictDesc As PICTDESC, riid As GUID, ByVal fOwn As Long, lplpvObj As Object) As Long
' Private Declare PtrSafe Function OleCreatePictureIndirect Lib "oleaut32.dll" (lpPictDesc As PICTDESC, riid As GUID, ByVal fOwn As Long, lplpvObj As Object) As Long
Private Declare PtrSafe Function OpenClipboard Lib "user32" (ByVal hWndNewOwner As Long) As Long
Private Declare PtrSafe Function CloseClipboard Lib "user32" () As Long
Private Declare PtrSafe Function GetClipboardData Lib "user32" (ByVal uFormat As Long) As Long
Const CF_ENHMETAFILE = 14
Private Declare PtrSafe Function CopyEnhMetaFile Lib "gdi32" Alias "CopyEnhMetaFileA" (ByVal hemfSrc As Long, ByVal lpszFile As String) As Long
Private Declare PtrSafe Function DeleteEnhMetaFile Lib "gdi32" (ByVal hemf As Long) As Long

Sub clip2emf()
    Dim hSrcMetaFile As Long '���������^�t�@�C���̃n���h��
    Dim hFileMetaFile As Long

    If OpenClipboard(0) Then
      hSrcMetaFile = GetClipboardData(CF_ENHMETAFILE)
      ' �n���h���𕡐����Ă���g�p����
      hSrcMetaFile = CopyEnhMetaFile(hSrcMetaFile, vbNullString)
      CloseClipboard
    End If

    If hSrcMetaFile = 0 Then
      MsgBox "emf�擾�Ɏ��s"
      Exit Sub
    End If

    fpath = ActiveWorkbook.Path & "\metafile.emf"
     '�t�@�C���ɕۑ�
    hFileMetaFile = CopyEnhMetaFile(hSrcMetaFile, fpath)
    '���^�t�@�C���̃N���[�Y
    DeleteEnhMetaFile hFileMetaFile
    DeleteEnhMetaFile hSrcMetaFile
End Sub


'' ���݂̃V�[�g�̑S�O���t��"chart001.png"�`���œ����ꏊ�ɏo��
Sub ExportAllChart()
    Dim cht, cht_i As Long
    Dim fpath As String

    cht_i = 0
    For Each cht In ActiveSheet.ChartObjects
        cht_i = cht_i + 1
        fpath = ActiveWorkbook.Path & "\chart" & Format(cht_i, "000") & ".png"
        cht.Chart.Export(fpath)
    Next cht
End Sub


'' ���݂̃V�[�g�̃O���t�̃f�[�^��u��
Sub ReplaceSeriesData(before As String, after as String)
    Dim cht As ChartObject
    Dim ser As Series

    For Each cht In ActiveSheet.ChartObjects
        For Each ser In cht.Chart.SeriesCollection
            ser.Formula = Replace(ser.Formula, before, after)
        Next
    Next
End Sub
