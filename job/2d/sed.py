#!/usr/bin/env python3
# coding: utf-8
# (File name: sed.py)
# Author: SENOO, Ken
# (Last update: 2015-01-16T17:21+09:00)
# License: MIT

"""
2次元河床変動計算の出力ををmaketecpt_cell_center.exeで処理したファイルのDZから区間堆積量[m3]を算出
入力：res*.end.dat.plt
出力：sed.csv
"""

import sys
import glob

argv = sys.argv
argc = len(argv)

## 計算結果から値を取得
if argc >= 2:
    FR = argv[1]
else:
    FR=glob.glob("./res*.end.dat.plt")[0]

with open(FR, "U", encoding="utf-8") as fr:
    fr = fr.read().splitlines()

## get variable names
var_names = fr[1].split()[2:]
var_names[:] = [i.strip('",') for i in var_names]

## get max column and row
max_col, max_row = list(map(int, fr[2].split()[2::2]))
var_array={}
for var_i, var in enumerate(var_names):
    if var_i <= 1: # 点の変数
        var_array[var] = [list(map(float, i.split())) for i in fr[4 + var_i * max_row:4 + (var_i + 1) * max_row]]
    elif var == "DZ": # セルの変数
        var_array[var] = [list(map(float, i.split())) for i in fr[2+4 + var_i * (max_row - 1) :2+4 + (var_i + 1) * (max_row -1 )]]

xmesh = var_array["X"]
ymesh = var_array["Y"]

sed_seg = []
segment =[115, 170] # ここで区間をメッシュの行番号で指定
segment.append(max_row-1)

nrow = 0
sed_area_sum = 0
tot_area = 0
for row in range(max_row - 1):
    nrow += 1
    for col in range(max_col - 1):
        area=-0.5 * sum([
            xmesh[row][col]     * ymesh[row][col+1]-xmesh[row][col+1]     * ymesh[row][col],
            xmesh[row][col+1]   * ymesh[row+1][col+1]-xmesh[row+1][col+1] * ymesh[row][col+1],
            xmesh[row+1][col+1] * ymesh[row+1][col]-xmesh[row+1][col]     * ymesh[row+1][col+1],
            xmesh[row+1][col]   * ymesh[row][col]-xmesh[row][col]         * ymesh[row+1][col]
            ])
        sed_area_sum += area * var_array["DZ"][row][col]
        tot_area += area
    if nrow in segment:
        sed_seg.append(sed_area_sum)
        sed_area_sum = 0

with open("./sed.csv", "w", encoding="utf-8", newline="\n") as fw:
    fw.write("Section,Sedimet[m3]\n")
    # for idx, sed in enumerate(sed_seg):
    for seg, sed in zip(segment, sed_seg):
        fw.write(str(seg)+","+str(sed)+"\n")
        print(str(sed))
    else:
        fw.write("Total,"+str(sum(sed_seg)))
        print(str(sum(sed_seg)), end="")
