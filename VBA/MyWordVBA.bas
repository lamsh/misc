' (File name: MyWordVBA.bas)
' Author: SENOO, Ken
' LICENSE: CC0

Option Explicit


'' フィールドコードのテキスト化
Sub FieldCode2Text()
    ' 本文中のフィールドコードのテキスト化
    ActiveDocument.Fields.Unlink

    ' テキストボックス内のフィールドコードのテキスト化
    Dim shp As Shape
    For Each shp In ActiveDocument.Shapes
        If shp.Type = msoTextBox Then
            shp.TextFrame.TextRange.Fields.Unlink
        End If
    Next
End Sub
