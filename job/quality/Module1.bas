Attribute VB_Name = "Module1"
Option Explicit

Sub judgeSS()

' ���Ԓl�f�[�^���璴�ߓ������Z�o

' ���j
' �ŏ��̔N�ƍŌ�̔N���擾
' 1�N�̓������擾
' 1�N���ƂɃ��[�v���A���߉񐔂𔻒�

Dim LastRow As Long
Dim row As Long

Dim FirstYear As Integer
Dim LastYear As Integer

Const RowMargin As Integer = 1

LastRow = Cells(Rows.Count, 1).End(xlUp).row

FirstYear = Year(Cells(2, 1).Value)
LastYear = Year(Cells(LastRow, 1).Value)

Dim Counter As Long
Counter = 1

Dim IsOut As Boolean
IsOut = False

ReDim OutDay(LastYear - FirstYear + 1) As Integer
Dim NowYear, IndexYear, DayOfYear, NowDay, NowHour

For NowYear = FirstYear To LastYear
    IndexYear = NowYear - FirstYear

    ' �N�Ԃ̓����̎���
    If Day(DateAdd("d", -1, NowYear & "/3/1")) = 29 Then
        DayOfYear = 366
    Else
        DayOfYear = 365
    End If

    For NowDay = 1 To DayOfYear
        ' ���Ԃ��Ƃɔ���
        ' ������1�񂾂��J�E���g
        For NowHour = 0 To 23
            If (IsOut = False) And (Cells(RowMargin + Counter, 3).Value > 25) Then
                OutDay(IndexYear) = OutDay(IndexYear) + 1
                IsOut = True
            End If
            
            Counter = Counter + 1
        Next NowHour
        IsOut = False
        
    Next NowDay
    
    ' �������o��
    Debug.Print NowYear, OutDay(IndexYear)
Next NowYear

End Sub


