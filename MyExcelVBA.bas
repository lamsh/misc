' (File name: MyExcelVBA.bas)
' Author: SENOO, Ken
' LICENSE: CC0

Option Explicit


Sub AddNewSheet(sheet_name)
    ' シートがあれば削除して、新規作成。
    Dim ws
    Dim sheet_name

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
