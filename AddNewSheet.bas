' (File name: AddNewSheet.bas)
' Author: SENOO, Ken
' LICENSE: CC0
' (Last update: 2015-03-10T18:38+09:00)

Sub AddNewSheet(sheet_name)

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

End Sub
