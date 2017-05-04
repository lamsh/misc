#!/usr/bin/env python3
# coding: utf-8
# (File name: makeDmn.py)
# Author: SENOO, Ken
# (Last update: 2015-02-17T14:35+09:00)
# License: MIT

""" Description
BH.dmnを作成するプログラムである。

横断のDXFファイルの以下の画層から値を抽出
* cross-section
* baseline (最初の1点のみ)

入力：
* ./cross-section.dxf
* ./label-DL.csv

出力：
* ./BH.dmn

必要な設定：
以下の変数値を対応する縮尺に設定する。
HSCALE: 図面x方向の縮尺
VSCALE: 図面y方向の縮尺
実際の長さ=寸法/NのNがHSCALEとVSCASEの値
実際の長さが5 mで寸法線で図ると25だとSCALE=5
"""

import ezdxf
import sys

HSCALE=5
VSCALE=5

FR="./cross-section.dxf"
rdwg=ezdxf.readfile(FR)
rmodelspace=rdwg.modelspace()

query=rmodelspace.query('LWPOLYLINE POLYLINE[layer=="cross-section"]')

ncross_sec=len(query)
npoints=[]
cross_sec=[]

for polyline in query:
    with polyline.points() as points:
        npoints.append(len(points))
        cross_sec.append([list(i[:2]) for i in points])

## 実際の基準線の高さ
FR="./label-DL.csv"
with open(FR, "U", encoding="utf-8") as fr:
    label=fr.read().rstrip().split("\n")
    KP=[i.split(",")[0] for i in label[1:]]
    BlockD=list(map(float, [i.split(",")[1] for i in label[1:]]))
    realDL=list(map(float, [i.split(",")[2] for i in label[1:]]))

## 図面上の基準線の高さ
query=rmodelspace.query('LWPOLYLINE POLYLINE[layer=="baseline"]')
dwgDL=[]
for polyline in query:
    with polyline.points() as points:
        dwgDL.append(points[0][1])


# FW="./BH.csv"
# with open(FW, "wb") as fw:
#     for polyline in range(ncoross_sec):
#         fw.write(str(npoints[polyline])+"\n")
#         for point in cross_sec[polyline]:
#             fw.writelines(",".join(list(map(str, point)))+"\n")
# sys.exit()

## cross_secの向きを統一
for No in range(ncross_sec):
    polyline = cross_sec[No]
    if (polyline[-1][0] - polyline[0][0]) < 0:
        polyline.reverse()

## modify z scale
for polyline in range(ncross_sec):
    XBASE=cross_sec[polyline][0][0]
    for point in range(len(cross_sec[polyline])):
        # cross_sec[polyline][point][0]=(cross_sec[polyline][point][0]-cross_sec[polyline][0][0])/HSCALE
        cross_sec[polyline][point][0]=(cross_sec[polyline][point][0]-XBASE)/HSCALE
        cross_sec[polyline][point][1]=(cross_sec[polyline][point][1]-dwgDL[polyline])/VSCALE+realDL[polyline]

zstat=["No. DeltaD Distance Min Max Mean".split()]

FW="./BH.dmn"
with open(FW, "w", encoding="utf-8", newline="\n") as fw:
    for polyline in range(ncross_sec):
        ymin=min([i[1] for i in cross_sec[polyline]])
        ymax=max([i[1] for i in cross_sec[polyline]])
        ymean=sum([i[1] for i in cross_sec[polyline]])/len(cross_sec[polyline])
## キロポスト、区間距離、最小y座標値、点の数、1,点の数、1,点の数、1、点の数
        header="{KP:<10}{D:10.2f}{ymin:10.2f}{NP:5}{i:5}{NP:5}{i:5}{NP:5}{i:5}{NP:5}\n".format(KP=KP[polyline][:10],D=BlockD[polyline], ymin=ymin, NP=npoints[polyline], i=1)
        zstat.append([KP[polyline], str(BlockD[polyline]), str(sum(BlockD[:polyline+1])), str(ymin), str(ymax), str(ymean)])

        fw.write(header)
        for lb, point in enumerate(range(npoints[polyline]), start=1):
            line="{x:8.2f}{y:8.2f}".format(x=cross_sec[polyline][point][0], y=cross_sec[polyline][point][1])
            fw.write(line)
            if lb%5==0 or point==npoints[polyline]-1: fw.write("\n")

FW="./zstat.csv"
with open(FW, "w", encoding="utf-8", newline="\n") as fw:
    fw.write("\n".join([",".join(zstat[i]) for i in range(len(zstat))]))
