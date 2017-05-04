#!/usr/bin/env python3
# coding: utf-8
# (File name: check-bounds.py)
# Author: SENOO, Ken
# License: MIT
# (Last update: 2015-01-16T18:56+09:00)

"""
以下のファイルをDXFに出力
* bounds.csv
* xybdsec.csv
* cross_sec.csv
"""
import ezdxf
import os

dwg=ezdxf.new()
modelspace=dwg.modelspace()
dwg.layers.create("bounds", {"color": 5})
dwg.layers.create("xybdsec", {"color": 5})
dwg.layers.create("cross-section", {"color": 5})

BOUNDS="./bounds.csv"
if os.path.exists(BOUNDS):
    with open(BOUNDS, "U", encoding="utf-8") as fr:
        fr=fr.read().rstrip().split("\n")
        nline=1
        nbounds=int(fr[0])
        bounds=[[] for i in range(nbounds)]
        for bound in range(nbounds):
            no, npoint=list(map(int, fr[nline].split(",")))
            nline+=1
            bounds[bound].extend([list(map(float, fr[nline+point].split(","))) for point in range(npoint)] )

            print(bound)
            nline+=npoint

    for bound in range(nbounds):
        modelspace.add_polyline2d(bounds[bound], dxfattribs={"layer": "bounds"})


XYBDSEC="./xybdsec.csv"
if os.path.exists(XYBDSEC):
    with open(XYBDSEC, "U", encoding="utf-8") as fr:
        fr=fr.read().rstrip().split("\n")
        nline=1
        nxybdsec=int(fr[0])
        xybdsec=[[] for i in range(nxybdsec)]
        for polyline in range(nxybdsec):
            npoint, no=list(map(int, fr[nline].split(",")))
            nline+=1
            xybdsec[polyline].extend([list(map(float, fr[nline+point].split(","))) for point in range(npoint)] )

            nline+=npoint

    for polyline in range(nxybdsec):
        modelspace.add_polyline2d(xybdsec[polyline], dxfattribs={"layer": "xybdsec"})


CROSS_SEC="./cross_sec.csv"
if os.path.exists(CROSS_SEC):
    with open(CROSS_SEC, "rU", encoding="utf-8") as fr:
        fr=fr.read().rstrip().split("\n")
        ncross_sec=int(fr[0].split(",")[0]) if "," in fr[0] else int(fr[0])
        cross_sec=[[] for i in range(ncross_sec)]
        for polyline in range(ncross_sec):
            cross_sec[polyline].append(list(map(float, fr[polyline+1].split(",")[1:3])))
            cross_sec[polyline].append(list(map(float, fr[polyline+1].split(",")[4:])))

    for polyline in range(ncross_sec):
        # modelspace.add_polyline2d(cross_sec[polyline])
        modelspace.add_polyline2d(cross_sec[polyline], dxfattribs={"layer": "cross-section"})

dwg.saveas("./bounds-check.dxf")
