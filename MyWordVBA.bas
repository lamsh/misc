' (File name: MyWordVBA.bas)
' Author: SENOO, Ken
' LICENSE: CC0

Option Explicit


'' �t�B�[���h�R�[�h�̃e�L�X�g��
Sub FieldCode2Text()
    ' �{�����̃t�B�[���h�R�[�h�̃e�L�X�g��
    ActiveDocument.Fields.Unlink

    ' �e�L�X�g�{�b�N�X���̃t�B�[���h�R�[�h�̃e�L�X�g��
    Dim shp As Shape
    For Each shp In ActiveDocument.Shapes
        If shp.Type = msoTextBox Then
            shp.TextFrame.TextRange.Fields.Unlink
        End If
    Next
End Sub
