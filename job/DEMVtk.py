#!/usr/bin/env python2.7
# coding: utf-8
# (File name: DEMVtk.py)
# Author: SENOO, Ken
# (Last Update: 2014-10-21T11:12+09:00)

"""
津波の地形データを開いてParaviewで表示させるためにVTKの形式で保存する。
* 
     imax= 1500,jmax=990, dx=dy=810.0m
     座標原点　X=-487200.0 Y=-371700.0

999.00: 冠水なし（陸地）
0.00: 冠水なし（水域）
i=j=1: 原点
座標原点　X=-7410.0 Y=-254950.0

データファイルの並び順番
j/i    1    imax
jmax: 左上 右上
...........
1:      左下 右下
本来なら990列である。データは可視性のため10列ごとに区切られている。

imax= 1500;jmax=990
ip=10
do is=1,imax,ip
    ie=min0(is+ip-1,imax)
    do j=jmax,1,-1
        read(03,'(10f8.2)') (dep(i,j),i=is,ie) 
    enddo
enddo
"""

import pyvtk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

FR="./Osaka_D05.dep"

delim=[8]*10
with open(FR) as f:
    IMAX, JMAX=map(int, f.readline().split())
    XORIG, YORIG, DELTA, HATENA=map(float, f.readline().split())
DX=DY=DELTA
# DEM=np.loadtxt(FR, skiprows=2,delimiter=delim)
DEM=np.genfromtxt(FR, skip_header=2,delimiter=delim)
# DEM=pd.read_fwf(FR, skiprows=2, widths=delim, header=None)
# DEM=DEM.values.reshape(-1, 990)
# 標高は負号が逆になっているので元に戻す。
# DEM=-DEM.reshape(JMAX, -1)
for column in range(IMAX/10):
    if column==0:
        DEM=-pd.read_fwf(FR, skiprows=2+column*JMAX, nrows=JMAX, widths=delim, header=None).values
        # DEM=np.genfromtxt(FR, skip_header=2+column*JMAX,delimiter=delim)
    else:
        DEM=np.column_stack([DEM, -pd.read_fwf(FR, skiprows=2+column*JMAX, nrows=JMAX, widths=delim, header=None).values])

X=np.arange(XORIG, XORIG+IMAX*DX, DX)
Y=np.arange(YORIG+JMAX*DY, YORIG, -DY)

X,Y=np.meshgrid(X, Y)
## [[(x, y, z), (x, y, z), ..., (x, y, z)]]
XYDEM=np.dstack([X,Y,DEM])
# sys.exit()

# ## データ確認のため図に出力
# plt.clf()
# plt.contourf(X,Y,DEM)
# plt.colorbar()
# plt.xlabel("X [m]")
# plt.ylabel("Y [m]")
# plt.title("Nankai DEM [m]")
# plt.savefig("./DEM.png", bbox_inches="tight")

## ポリゴンの構成ノード番号。時計回りにつける
# polygon= [[ IMAX*(j)+i, IMAX*(j)+i+1,  IMAX*(j+1)+i+1, IMAX*(j+1)+i]
#     # UL, UR LR, LLの順番。
#     for j in range(JMAX-1-1, -1, -1)  for i in range(IMAX-1)]

XYDEM=XYDEM.reshape(-1,3).tolist() # listにしたほうが早い
# structure=pyvtk.PolyData(points=XYDEM.reshape(-1, 3), polygons= polygon)
structure=pyvtk.StructuredGrid((IMAX, JMAX, 1), XYDEM)
pointdata=pyvtk.PointData(pyvtk.Scalars(DEM.reshape(-1), name="DEM[m]", lookup_table="default"))

# cellvalue=[sum([XYDEM[i][2]  for i in j])/4.0 for j in polygon]
# celldata=pyvtk.CellData( pyvtk.Scalars(cellvalue, name="DEM[m]", lookup_table="default"))
vtk=pyvtk.VtkData(structure, "# terrestrial data for tsunami", pointdata )
vtk.tofile("DEM", "binary")
