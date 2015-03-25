' (File name: MyExcelVBA.bas)
' Author: SENOO, Ken
' LICENSE: CC0

Option Explicit


Sub AddNewSheet(sheet_name as String)
    ' シートがあれば削除して、新規作成。
    Dim ws
    For Each ws In Worksheets
        If ws.Name = sheet_name Then
            Application.DisplayAlerts = False
            ws.Delete
            Application.DisplayAlerts = True
        End If
    Next ws

    ' 右隣に新規シートを追加。
    Sheets.Add(After:=ActiveSheet).Name = sheet_name
End Sub


'' VBAではサイズの単位はpt。このptは以下の対応となっている
'' 72 pt = 25.4 mm

'' Application.CentimetersToPointsと同じ
Function cm2pt(cm as Double) as Double
    cm2pt = 72/25.4 * 10 * cm
End Function

'' Application.InchesToPointsと同じ
Function pt2cm(pt as Double) as Double
    pt2cm = 0.1 * 25.4 / 72 * pt
End Function


'' クリップボードの内容を同じ場所のmetafile.emfに保存
''' TODO: Chart.CopyPictureで直接保存できない。手作業でコピーしないとファイルに保存できない。
''' 複数のグラフを選択すると矩形領域でまとめて保存できる。

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
    Dim hSrcMetaFile As Long '複製元メタファイルのハンドル
    Dim hFileMetaFile As Long

    If OpenClipboard(0) Then
      hSrcMetaFile = GetClipboardData(CF_ENHMETAFILE)
      ' ハンドルを複製してから使用する
      hSrcMetaFile = CopyEnhMetaFile(hSrcMetaFile, vbNullString)
      CloseClipboard
    End If

    If hSrcMetaFile = 0 Then
      MsgBox "emf取得に失敗"
      Exit Sub
    End If

    fpath = ActiveWorkbook.Path & "\metafile.emf"
     'ファイルに保存
    hFileMetaFile = CopyEnhMetaFile(hSrcMetaFile, fpath)
    'メタファイルのクローズ
    DeleteEnhMetaFile hFileMetaFile
    DeleteEnhMetaFile hSrcMetaFile
End Sub


'' 現在のシートの全グラフを"chart001.png"形式で同じ場所に出力
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


'' 現在のシートのグラフのデータを置換
Sub ReplaceSeriesData(before As String, after as String)
    Dim cht As ChartObject
    Dim ser As Series

    For Each cht In ActiveSheet.ChartObjects
        For Each ser In cht.Chart.SeriesCollection
            ser.Formula = Replace(ser.Formula, before, after)
        Next
    Next
End Sub
