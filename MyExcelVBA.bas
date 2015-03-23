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
