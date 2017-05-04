Attribute VB_Name = "Module1"
Option Explicit

Sub judgeSS()

' 時間値データから超過日数を算出

' 方針
' 最初の年と最後の年を取得
' 1年の日数を取得
' 1年ごとにループし、超過回数を判定

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

    ' 年間の日数の収得
    If Day(DateAdd("d", -1, NowYear & "/3/1")) = 29 Then
        DayOfYear = 366
    Else
        DayOfYear = 365
    End If

    For NowDay = 1 To DayOfYear
        ' 時間ごとに判定
        ' 同日は1回だけカウント
        For NowHour = 0 To 23
            If (IsOut = False) And (Cells(RowMargin + Counter, 3).Value > 25) Then
                OutDay(IndexYear) = OutDay(IndexYear) + 1
                IsOut = True
            End If
            
            Counter = Counter + 1
        Next NowHour
        IsOut = False
        
    Next NowDay
    
    ' 日数を出力
    Debug.Print NowYear, OutDay(IndexYear)
Next NowYear

End Sub


