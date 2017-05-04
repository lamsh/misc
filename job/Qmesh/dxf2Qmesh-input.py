#!/usr/bin/env python3
# coding: utf-8
# (File name: dxf2Qmesh-input.py)
# Author: SENOO, Ken
# (Last update: 2015-01-02T17:29+09:00)
# License: MIT

"""
以下のファイルをDXFに出力
* bounds.csv
* xybdsec.csv
# * cross_sec.csv

== polycy
* open DXF.
* get bounds, xybdsec, cross_sec point value.
* smoothing bounds
* output bounds-src,bounds,xybdsec,cross_sec to DXF
* output {bounds,xybdsec,cross_sec}.csv for Qmesh
cross_secはまだ未実装

== Caution
入力のDXFデータは
* 対応するレイヤ名で作ること
* プロットの順番を守ること。
"""

import ezdxf
import os
import csv

import scipy.interpolate as ip
import numpy as np
# import matplotlib.pyplot as plt
import sys

## open DXF
FR="./input.dxf"
rdwg=ezdxf.readfile(FR)
rmodelspace=rdwg.modelspace()

wdwg=ezdxf.new()
wmodelspace=wdwg.modelspace()
wdwg.layers.create("bounds-src", {"color": 7})
wdwg.layers.create("bounds", {"color": 5})
wdwg.layers.create("xybdsec", {"color": 5})
# wdwg.layers.create("cross-section", {"color": 4})

bounds=[]
bcount=0

xybdsec=[]
xycount=0

for entity in rmodelspace:
    if "XYBDSEC" in entity.dxf.layer.upper():
        xybdsec.append([])
        if entity.dxftype() == "LWPOLYLINE":
            for point in entity.get_points():
                xybdsec[xycount].append(list(point[:2]))
        elif entity.dxftype() == "POLYLINE":
            for point in entity.points():
                xybdsec[xycount].append(list(point[:2]))
        xycount+=1

    if "BOUND" in entity.dxf.layer.upper():
        bounds.append([])
        if entity.dxftype() == "LWPOLYLINE":
            for point in entity.get_points():
                bounds[bcount].append(list(point[:2]))
        elif entity.dxftype() == "POLYLINE":
            for point in entity.points():
                bounds[bcount].append(list(point[:2]))
        bcount+=1
# sys.exit()

nbounds=len(bounds)
nxybdsec=len(xybdsec)
# ncross_sec=len(cross_sec)

## remove duplicate value
for polyline in range(nbounds):
    for index, elem in enumerate(bounds[polyline]):
        if bounds[polyline].count(elem) >= 2:
            del bounds[polyline][index]

for polyline in range(nxybdsec):
    for index, elem in enumerate(xybdsec[polyline]):
        if xybdsec[polyline].count(elem) >= 2:
            del xybdsec[polyline][index]
# for polyline in range(ncross_sec):
#     for index, elem in enumerate(cross_sec[polyline]):
#         if cross_sec[polyline].count(elem) >= 2:
#             del cross_sec[polyline][index]

## replace first/last xybdsec value to bounds value
if len(xybdsec) == 0: xybdsec=[[],[]]
# xybdsec[0]=[bounds[i][0] for i in range(nbounds)]
# xybdsec[-1]=[bounds[i][-1] for i in range(nbounds)]
# nxybdsec=len(xybdsec)
# sys.exit()

## xybdsecの最初と最後の値をboundsの値と比較して違ったら追加。似ていたら上書き
for polyline in range(nbounds):
    if len(xybdsec[0]) == 0:
        xybdsec[0]=[bounds[i][0] for i in range(nbounds)]
        xybdsec[-1]=[bounds[i][-1] for i in range(nbounds)]
    else:
        if abs(sum(np.array(xybdsec[0][polyline])-np.array(bounds[polyline][0]))) <= abs(0.1):
            xybdsec[0]=[bounds[i][0] for i in range(nbounds)]
        else:
            xybdsec[:0]=[[bounds[i][0] for i in range(nbounds)]]

        if abs(sum(np.array(xybdsec[-1][polyline])-np.array(bounds[polyline][-1]))) <= abs(0.1):
            xybdsec[-1]=[bounds[i][-1] for i in range(nbounds)]
        else:
            xybdsec.append([bounds[i][-1] for i in range(nbounds)])

nxybdsec=len(xybdsec)

## smoothing bounds
sbounds=[]
for bound in range(nbounds):
    xpoints=[bounds[bound][i][0] for i in range(len(bounds[bound]))]
    ypoints=[bounds[bound][i][1] for i in range(len(bounds[bound]))]

    # spline parameters
    s=0.0 # smoothness parameter
    k=2 # spline order
    nest=-1 # estimate of number of knots needed (-1 = maximal)
    # find the knot points
    tckp,u = ip.splprep([xpoints,ypoints],s=s,k=k,nest=nest)

    xnew,ynew = ip.splev(np.linspace(0,1,2000),tckp)
    xy_spl=[[i,j] for i,j in zip(xnew,ynew)]
    sbounds.append(xy_spl)
    # spl=dxf.w_polyline(xy_spl,'%s_1'%lname)

## 始点と終点はもとの座標と一致させる
for polyline in range(nbounds):
    sbounds[polyline][0] = xybdsec[0][polyline]
    sbounds[polyline][-1] = xybdsec[-1][polyline]

## output DXF
if nbounds != 0:
    for polyline in range(nbounds):
        wmodelspace.add_polyline2d(bounds[polyline], dxfattribs={"layer": "bounds-src"})
        wmodelspace.add_polyline2d(sbounds[polyline], dxfattribs={"layer": "bounds"})

if nxybdsec != 0:
    for polyline in range(nxybdsec):
        wmodelspace.add_polyline2d(xybdsec[polyline], dxfattribs={"layer": "xybdsec"})

# if ncross_sec != 0:
#     for polyline in range(ncross_sec):
#         modelspace.add_polyline2d(cross_sec[polyline], dxfattribs={"layer": "cross_sec", "color": 5})

wdwg.saveas("./mesh-outline.dxf")


## output csv for Qmesh
# fw= open("./bounds.csv", "w", encoding="utf-8", newline="")

with open("./bounds.csv", "w", encoding="utf-8", newline="") as fw:
    writer=csv.writer(fw)
    writer.writerow([nbounds])
    for no in range(nbounds):
        writer.writerow([no+1, len(sbounds[no])])
        writer.writerows(sbounds[no])

fw= open("./bounds-src.csv", "w", newline="")
writer=csv.writer(fw)
with fw:
    writer.writerow([nbounds])
    for no in range(nbounds):
        writer.writerow([no+1, len(bounds[no])])
        writer.writerows(bounds[no])

fw= open("./xybdsec.csv", "w", newline="")
writer=csv.writer(fw)
with fw:
    writer.writerow([nxybdsec])
    for no in range(nxybdsec):
        writer.writerow([len(xybdsec[no]), no+1])
        writer.writerows(xybdsec[no])
