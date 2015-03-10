' (File name: AddNewSheet.bas)
' Author: SENOO, Ken
' LICENSE: CC0
' (Last update: 2015-03-10T18:38+09:00)

Sub AddNewSheet(sheet_name)

' �V�[�g������΍폜���āA�V�K�쐬�B
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
