#!/usr/bin/env python2.7
# coding: utf-8
# (File name: TsunamiVtk.py)
# Author: SENOO, Ken
# (Last Update: 2014-10-21T11:11+09:00)
# Lincense: MIT

"""
津波の計算結果を開いてParaviewで表示させるためにVTKの形式で保存する。
* データは60 s = 1 minごとのデータ
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
"""

import pyvtk
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

## 地形データから原点座標と間隔を取得
with open("../Osaka_D05.dep") as fr:
    IMAX, JMAX=map(int, fr.readline().split())
    XORIG, YORIG, DELTA, HATENA=map(float, fr.readline().split())
DX=DY=DELTA
X=np.arange(XORIG, XORIG+IMAX*DX, DX)
Y=np.arange(YORIG, YORIG+JMAX*DY, DY)
X,Y=np.meshgrid(X, Y)

FR=u"./Osaka_case03_3分破堤.suf"


delim=[7]*10
nrow=IMAX*JMAX/10
preTsunami=[[] for i in range(nrow)]

time1=time.clock()
with open(FR, "U") as fr:
    for index, step in enumerate(range(1081)):
        ## 時間ステップごとのヘッダー部の読み飛ばし
        if index==0:
            ## 1行の文字数を取得
            # rowcol=len(fr.readline().rstrip())
            # rowcol=len(fr.next().rstrip())
            rowcol=70
            ## 途中の時間ステップからも読めるようにシーク位置を指定
            fr.seek(0)
            fr.seek((nrow+1)*(rowcol+2)*step)
        fr.next()

        ## 1行ずつデータを読んで列ごと(7文字区切り)にリストに格納
        for row in range(nrow):
            line=fr.next().rstrip()
            preTsunami[row]=[line[i:i+7] for i in range(0, rowcol, 7)]

        ## リストを配列化
        Tsunami=np.array(preTsunami,dtype=np.float).reshape(-1, IMAX)
        Tsunami[Tsunami==999.000]=0.0 # fill missing value

        ## [[(x, y, z), (x, y, z), ..., (x, y, z)]]
        XYTsunami=np.dstack([X,Y,Tsunami])

        # ## matplotlibで2Dコンター図の描画
        # PARAMS={
        # "lines.linewidth": 2,
        # "axes.labelsize": 14,
        # "legend.fontsize": 14,
        # # "axes.grid": True,
        # }
        # plt.rcParams.update(PARAMS)
        #
        # plt.ion()
        # plt.clf()
        # plt.contourf(X,Y,Tsunami)
        # plt.colorbar()
        # plt.xlabel("X [m]")
        # plt.ylabel("Y [m]")
        # plt.title("Nankai Tsunami [m]")
        #
        # fname="Tsunami-{step:03}".format(step=step)
        # plt.savefig(fname+".png", bbox_inches="tight")


        ## format for VTK
        ### polygonの構成ノードを格納
        # polygon= [[ IMAX*(j)+i, IMAX*(j)+i+1, IMAX*(j+1)+i+1, IMAX*(j+1)+i ]
        #     # UL, UR LR, LLの順番。 端を除外
        #     for j in range(JMAX-1-1, -1, -1)  for i in range(IMAX-1)]

        XYTsunami=XYTsunami.reshape(-1,3).tolist() # listにしたほうが早い
        # structure=pyvtk.PolyData(points=XYTsunami.reshape(-1, 3), polygons= polygon)

        ## VTK用にデータを用意
        structure=pyvtk.StructuredGrid((IMAX, JMAX, 1), XYTsunami)
        pointdata=pyvtk.PointData(pyvtk.Scalars(Tsunami.reshape(-1), name="Tsunami[m]", lookup_table="default"))
        # structure=pyvtk.PolyData(points=XYTsunami, polygons= polygon)
        # pointdata=pyvtk.PointData(pyvtk.Scalars(Tsunami.reshape(-1), name="Tsunami[m]", lookup_table="default"))
        # cellvalue=[sum([XYTsunami[i][2]  for i in j])/4.0 for j in polygon]

        # celldata=pyvtk.CellData(pyvtk.Scalars(cellvalue, name="Tsunami[m]", lookup_table="default"))
        # vtk=pyvtk.VtkData(structure, "# Water height data for Nankai tsunami", celldata, pointdata )
        vtk=pyvtk.VtkData(structure, "# Water height data for Nankai tsunami", pointdata)

        ## 時間ステップをファイル名末尾につけて保存
        fname="Tsunami-{step:04}".format(step=step)
        vtk.tofile(fname, "binary")

        time2=time.clock()
        print("output {step:04} min. elapsed {second} s".format(step=step, second=time2-time1))
