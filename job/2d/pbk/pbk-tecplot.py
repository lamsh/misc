#!/usr/bin/env python3
# coding: utf-8
# (File name: pbk-tecplot.py)
# Author: SENOO, Ken
# (Last update: 2015-01-16T18:16+09:00)
# License: MIT

"""以下のファイルから平均粒径の平面分布図のtecplotファイルを作成
* bed.dat
* pbk.dat
* xyeh.dat
"""
import numpy as np
import sys


def getEncode(filepath):
    encs = "utf-8 sjis".split()
    for enc in encs:
        with open(filepath, encoding=enc) as fr:
            try:
                fr = fr.read()
            except UnicodeDecodeError:
                continue
        return enc

## 代表粒径を取得
FR="./bed.dat"
with open(FR, "U", encoding=getEncode(FR)) as fr:
    dm=list(map(float, fr.readlines()[12].split()[:-1]))
    dm_level=len(dm)

## メッシュ番号ごとの代表粒径の存在割合を取得
FR="./pbk.dat"
with open(FR, "U", encoding="utf-8") as fr:
    imax, jmax=list(map(int, fr.readline().split()))[:2]

## pbkファイルの読み込み
pbk=np.genfromtxt(FR, skip_header=1)

## 先頭列を追加
begin_col_pbk = pbk[::jmax].copy()
begin_col_pbk[:, 1] = 1
pbk=np.insert(pbk, range(0, len(pbk), jmax), begin_col_pbk, axis = 0)

## 先頭行を追加
begin_row_pbk = pbk[:jmax+1].copy()
begin_row_pbk[:, 0] = 1
pbk=np.insert(pbk, 0, begin_row_pbk, axis = 0)

# sys.exit()
## 平均粒径の算出
pbk[:, 2:]=pbk[:, 2:] * dm * 0.01
mean_dm=pbk[:, 2:].sum(axis=1)


## 地形のxyzの取得
FR="./xyeh.dat"
xyeh=np.genfromtxt(FR, skip_header=1)

## tecplotは列が先なので修正
xyeh=np.vstack([xyeh[col::jmax+1] for col in range(jmax+1)])
mean_dm=np.hstack([mean_dm[col::jmax+1] for col in range(jmax+1)])

xyeh_x=xyeh[:,2]
xyeh_y=xyeh[:,3]
xyeh_z=xyeh[:,4]


## tecplot形式で出力
FW="DM.plt"
with open(FW, "w", encoding="utf-8", newline="\n")  as fw:
    HEADER="""TITLE     = "tecplot"
VARIABLES = "X"
"Y"
"Z"
"DM"
ZONE T="ZONE 001"
 STRANDID=0, SOLUTIONTIME=0
 I={i}, J={j}, K=1, ZONETYPE=Ordered
 DATAPACKING=POINT
""".format(i=imax+1, j=jmax+1)
    fw.write(HEADER)
with open(FW, "ab")  as fw:
    np.savetxt(fw, np.column_stack([xyeh_x, xyeh_y, xyeh_z, mean_dm]))
