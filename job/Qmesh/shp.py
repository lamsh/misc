#!/usr/bin/env python3
# coding: utf-8
# (File name: shp.py)
# Author: SENOO, Ken
# (Last update: 2015-01-16T18:44+09:00)
# License: MIT

"""
メッシュデータ"mesh.dat"をGISで使えるシェープファイルに変換
"""

import shapefile
import pandas as pd
import sys
import os


def getPRJwkt(epsg):
   """
   Grab an WKT version of an EPSG code
   usage getPRJwkt(4326)

   This makes use of links like http://spatialreference.org/ref/epsg/4326/prettywkt/
  JGD2000 / Japan Plane Rectangular CS I: 2443
   """

   import urllib
   f=urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg))
   return f.read()

XMARGIN=0
YMARGIN=0
EPSG_CODE=0

# XMARGIN=96648
# YMARGIN=206282
# EPSG_CODE=2451

FR="./mesh.dat"

mesh=pd.read_table(FR,skiprows=1, header=None, sep="\s+")
HEADER="row col x y z orth".split()
mesh.columns=HEADER

OUTDIR="./shp/"
FW="mesh"

if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

imax=mesh.row.max()
jmax=mesh.col.max()

xmesh=mesh.x.reshape(-1, jmax)
ymesh=mesh.y.reshape(-1, jmax)
zmesh=mesh.z.reshape(-1, jmax)

# wshp=shapefile.Writer(shapeType=3)
wshp=shapefile.Writer(shapefile.POLYGON)
# wshp=shapefile.Writer()
wshp.field("NUMBER","N", 10, 0)
wshp.field("ROW","N", 10, 0)
wshp.field("COLUMN","N", 10, 0)
wshp.field("DEM","F", 10, 5)

## line shapefile
# for i in range(imax):
# for j in range(jmax):
#     # wshp.line(shapeType=shapefile.POLYLINE, parts=[zip(xmesh[i, :], ymesh[i, :])])
#     wshp.line(parts=[zip(xmesh[j, :], ymesh[j, :])])
#     wshp.record("VERTICAL")

# for i in range(imax):
#     wshp.poly(shapeType=shapefile.POLYLINE, parts=[zip(xmesh[:, i], ymesh[:, i])])
#     wshp.record("HORIZONTAL")


xmesh_lis=(xmesh+XMARGIN).tolist()
ymesh_lis=(ymesh+YMARGIN).tolist()
zmesh_lis=(zmesh).tolist()


num=0
for col in range(jmax-1):
    for row in range(imax-1):
        num+=1
        wshp.poly(parts=[[
            [ xmesh_lis[row][col], ymesh_lis[row][col] ],
            [ xmesh_lis[row][col+1], ymesh_lis[row][col+1] ],
            [ xmesh_lis[row+1][col+1], ymesh_lis[row+1][col+1] ],
            [ xmesh_lis[row+1][col], ymesh_lis[row+1][col] ],
            [ xmesh_lis[row][col], ymesh_lis[row][col]]]]
            )
        center=sum([
                zmesh_lis[row][col],
                zmesh_lis[row][col+1],
                zmesh_lis[row+1][col+1],
                zmesh_lis[row+1][col]]) / 4
        wshp.record(num, row+1, col+1, center)
        # wshp.record(row+col)
        # wshp.record(row+col)

wshp.save(OUTDIR+FW)
with open(OUTDIR+FW+".prj", "w", encoding="utf-8", newline="\n") as fw: fw.write(getPRJwkt(EPSG_CODE))
