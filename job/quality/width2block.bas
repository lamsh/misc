' (File name: width2block.bas)
' Author: SENOO, Ken
' LICENSE: CC0
' (Last update: 2015-03-03T17:49+09:00)

Sub width2block()
  ' with.prnのシートで実行すると右隣にblockシートを作り、そこにブロック分割図の形式で出力
  ' width.prn形式のシートからブロック分割図の形式に変換
  ' 流れ：
  ' 1. ブロック分割用のシートを作成
  ' 2. シートに値を書き込む

' 元データのシート
Set DataSheet = ActiveSheet

sheet_name = "block"

' シートがあれば削除して、新規作成。
For Each ws In Worksheets
  If ws.Name = sheet_name Then
    Application.DisplayAlerts = False
    ws.Delete
    Application.DisplayAlerts = True
  End If
Next ws

' 右隣に新規シートを追加。
Sheets.Add(After:=ActiveSheet).Name = sheet_name

' ' シートがあればそれをアクティブにし、なければ新規作成。
' IsExist = False
' For Each ws In Worksheets
'   If ws.Name = sheet_name then
'     ActiveSheet.Name = ws.Name
'     IsExist = True
'   End If
' Next ws

' ' 右端に新規シートを追加。
' If Not IsExist Then
'   Sheets.Add(After := Sheets(Sheets.Count)).Name = sheet_name
' End If

Set BlockSheet = ActiveSheet


I_POS = "B2"
J_POS = "C2"

MAX_I = DataSheet.Range(I_POS)
MAX_J = DataSheet.Range(J_POS)

MARGIN_X = 2
MARGIN_Y = 4

For i = 1 To MAX_I
  For j = 1 To MAX_J
    myWidth = DataSheet.Range("D" & ((i - 1) * MAX_J + j + 3))
    BlockSheet.Cells(MAX_J - j + 1 + MARGIN_Y, i + MARGIN_X).Value = myWidth
  Next j
Next i

End Sub
