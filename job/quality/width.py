#!/usr/bin/env python3
# coding: utf-8
# (File name: width.py)
# Author: SENOO, Ken
# License: MIT
# (Last update: 2015-01-26T15:44+09:00)

"""
Excelの地形データからwidth.prnを作成する
入力：input.xls
出力：width.prn
"""

import sys

import xlrd

FR = "./input.xls"

START_ROW = 5
START_COL = 4

MAX_NO = 35  # No.の個数
MAX_HEIGHT_INDEX = 32  # 標高の個数

BLOCK_ID = 1

## ファイル取得
wb = xlrd.open_workbook(FR)
sheet_name = wb.sheet_names()

ws = wb.sheet_by_index(0)

width_list = []  # 書き込み用データの格納

for row in range(MAX_HEIGHT_INDEX):
    width_list.append([-999.0] + ws.row_values(row + START_ROW, START_COL-1))

width_list.append([-999.0]*(len(width_list[0])))
width_list[:] = width_list[::-1]


## ファイル出力

FW = "./width.prn"

header = [
            ["block-no", "mi", "mj"],
            [BLOCK_ID, MAX_NO+1, MAX_HEIGHT_INDEX+1],
            ["k", "i", "j", "width"],
        ]

whead = "\n".join(["\t".join(map(str,row)) for row in header])+"\n"

## 転置
width_list = list(map(list, zip(*width_list)))


## 0の値は-999.0に置換
for row in range(len(width_list)):
    for col in range(len(width_list[row])):
        if width_list[row][col] == 0:
            width_list[row][col] = -999.0

wval = []
for ri, row in enumerate(width_list, start=1):
    for ci, col in enumerate(row, start=1):
        wval.append("{k}\t{x}\t{y}\t{width}".format(k=BLOCK_ID, x=ri, y=ci, width=col))




with open(FW, "w", encoding="utf-8", newline="\n") as fw:
    fw.write(whead)
    fw.write("\n".join(wval))


## 5以下の値を-999.0、5-10を10に mask
for row in range(len(width_list)):
    for col in range(len(width_list[row])):
        if width_list[row][col] <= 5:
            width_list[row][col] = -999.0
        if 5 < width_list[row][col] < 10:
            width_list[row][col] = 10

wval = []
for ri, row in enumerate(width_list, start=1):
    for ci, col in enumerate(row, start=1):
        wval.append("{k}\t{x}\t{y}\t{width}".format(k=BLOCK_ID, x=ri, y=ci, width=col))

FW = "./width-masked.prn"
with open(FW, "w", encoding="utf-8", newline="\n") as fw:
    fw.write(whead)
    fw.write("\n".join(wval))
