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
