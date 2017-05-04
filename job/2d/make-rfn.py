#!/usr/bin/env python3
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2015-01-16T18:36+09:00)

FR="../xyeh.dat"

# with open(FR) as fr:
#     ROW, COL=map(int, fr.readline().split()[:2])

ROW=221; COL=41
FW="./rfn.dat"
with open(FW, "w", encoding="utf-8", newline="\n") as fw:
    value="{row:5}{col:5}\n".format(row=ROW, col=COL)
    fw.write(value)
    for row in range(2, ROW+1):
        for col in range(2, COL+1):
            value="{row:5}{col:5}{maning:10.3f}\n".format(row=row, col=col, maning=0.030)
            fw.write(value)
