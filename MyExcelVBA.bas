' (File name: MyExcelVBA.bas)
' Author: SENOO, Ken
' LICENSE: CC0

Option Explicit


Sub AddNewSheet(sheet_name)
    ' �V�[�g������΍폜���āA�V�K�쐬�B
    Dim ws
    Dim sheet_name

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
