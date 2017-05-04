#!/usr/bin/env python3
# coding: utf-8
# (File name: read-contour.py)
# Author: SENOO, Ken
# (Last update: 2015-01-16T18:39+09:00)
# License: MIT

""" Description
高さの情報を持ったDXFファイルから値を抽出し、点としてcsvかTecplotの形式に出力
"""
import ezdxf

FR="./contour.dxf"

rdwg = ezdxf.readfile(FR)
rmsp = rdwg.modelspace()
query = rmsp.query('LWPOLYLINE [layer == "contour"]')

contour = []
for polyline in query:
    elevation = polyline.dxf.elevation
    with polyline.points() as points:
        contour.append([list(i[:2]) + [elevation] for i in points])

## csv
# FW = "./xyz.csv"
# with open(FW, "wb") as fw:
#     header="X,Y,Z\n"
#     fw.writelines(header)
#     for polyline in contour:
#         for point in polyline:
#             fw.writelines(",".join(map(str, point))+"\n")

## Tecplot
FW = "./contour.plt"
with open(FW, "w", encoding="utf-8", newline="\n") as fw:
    npoint = sum([len(i) for i in contour])
    header="""TITLE     = ""
VARIABLES = "X"
"Y"
"Z"
ZONE T="ZONE 001"
STRANDID=0, SOLUTIONTIME=0
I={point}, J=1, K=1, ZONETYPE=Ordered
DATAPACKING=POINT
DT=(DOUBLE DOUBLE DOUBLE )
""".format(point = npoint)
    fw.writelines(header)

    for polyline in contour:
        for point in polyline:
            fw.writelines(",".join(list(map(str, point))) + "\n")
