#!/usr/bin/env python3
# coding: utf-8
# (File name: plot-mesh.py)
# Author: SENOO, Ken
# (Last Update: 2015-01-16T18:46+09:00)

""" descriptipn
Qmeshの出力であるmesh.datからmeshの画像とdxfを作成
input：./mesh.dat
output: ./mesh.{pdf,dxf}
"""

""" mesh.datのformat
number of i mesh, number of j mesh, 低水路境界ライン１のJ番号, 低水路境界ライン２のJ番号
i, j, x, y, z, accuracy
i=S
j=N
"""

import matplotlib.pyplot as plt
import pandas as pd
import ezdxf
import sys

FR="./mesh.dat"

MESH=pd.read_table(FR,skiprows=1, header=None, sep="\s+")
header="i j x y z orth".split()

MESH.columns=header

IMAX=MESH.i.max()
JMAX=MESH.j.max()

X=MESH.x.reshape(-1,JMAX)
Y=MESH.y.reshape(-1,JMAX)
Z=MESH.z.reshape(-1,JMAX)

plt.clf()
axis=plt.gca()
## each cell
# for i in range(IMAX-1):
#     for j in range(JMAX-1):
#         axis.add_patch(plt.Polygon([
#             ( X[i][j], Y[i][j] ), # upper left
#             ( X[i+1][j], Y[i+1][j] ), # lower left
#             ( X[i+1][j+1], Y[i+1][j+1] ), # lower right
#             ( X[i][j+1], Y[i][j+1] ), # upper right
#             ],
#             facecolor="None"))

for i in range(IMAX):
    plt.plot(X[i, :], Y[i, :], lw=0.1, color="k")

for j in range(JMAX):
    plt.plot(X[:, j], Y[:, j], lw=0.1, color="k")

plt.contourf(X, Y, Z)
# plt.colorbar(extend="both", orientation="hosizontal",  pad=0.05, fraction=0.09, aspect=10 )
plt.colorbar(extend="both", pad=0.05, fraction=0.09, aspect=10 )


axis.set_aspect("equal")
axis.autoscale_view()
plt.savefig("mesh.pdf", bbox_inches="tight")


## export DXF
drawing=ezdxf.new()
modelspace=drawing.modelspace()
LAYER="mesh"
drawing.layers.create(LAYER, {"color": 9})
dxfattribs={"layer": LAYER}
block_name="mesh"
block=drawing.blocks.new(block_name)
## リストでやるよりこっちのほうが早い
for i in range(IMAX):
    block.add_polyline2d(list(zip(X[i, :], Y[i, :])), dxfattribs=dxfattribs)
for j in range(JMAX):
    block.add_polyline2d(list(zip(X[:, j], Y[:, j])), dxfattribs=dxfattribs)
modelspace.add_blockref(block_name, [0,0], dxfattribs={"layer": LAYER})
drawing.saveas("./mesh.dxf")
