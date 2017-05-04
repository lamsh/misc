#!/usr/bin/env python3
# coding: utf-8
# (File name: BH2dxf-2D.py)
# Author: SENOO, Ken
# Lincense: MIT
# (Last update: 2015-02-17T19:25+09:00)

"""
横断のデータをCADのDXF形式に出力する。
EX_OUDANの代替となる。
同じディレクトリの以下の入出力ファイルを操作する。
入力：BH.dmnとcross_sec.csv、Mod_Basepoint.csv
出力：
* check-cross-section.dxf：横断をCADのdxfに出力。
* BH-mod.dmn：Mod_Basepoint.csvがあるときだけ、BH.dmnをシフトしたものを出力。
"""

import sys
import os

import ezdxf

class Point():
    def __init__(self, x=0, y=0, z=0, *args):
        self.x = x
        self.y = y
        self.z = z
        self.length = (self.x**2 + self.y**2 + self.z**2)**0.5

    def __str__(self):
        """str(Point)で出力"""
        return "Point({},{},{})".format(self.x, self.y, self.z)

    def __mul__(self, i):
        return Point(self.x * i, self.y * i, self.z * i)

    def __truediv__(self, i):
        return Point(self.x / i, self.y / i, self.z / i)

    def move(self, dx=0, dy=0, dz=0):
        self.x = self.x + dx
        self.y = self.y + dy
        self.z = self.z + dz

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx**2 + dy**2 + dz**2)**0.5

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def subtract(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z + other.z)

    def divide(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z + other.z)


INDIR="./"
DEM=INDIR+"BH.dmn"
CROSS=INDIR+"cross_sec.csv"
ModBase=INDIR+"Mod_Basepoint.csv"

DISTANCE_SCALE = 1  # 長さ方向のDXFの縮尺
DEPTH_SCALE = 1  # 深さ方向のDXFの縮尺

xz=[]
no=-1
demheader=[]
## まず横断のx-hデータを取得
# with open(DEM, "U", encoding="utf-8") as fr:
with open(DEM, "U") as fr:
    for line in fr:
        if not line[0].isspace(): # 1列目が空白以外はヘッダー。
            no+=1
            xz.append([])
            demheader.append(line)
        else:
            # xz[no].extend(map(float, line.split()))
            xz[no].extend(map(float, [line[i:i+8] for i in range(0, len(line)-1, 8)]))

## 横断の格納。xz[横断番号].{x,y}
for no_i, no in enumerate(xz):
    xz[no_i] = [Point(x, 0, z) for x, z in zip(no[::2], no[1::2])]

## 始点と終点の取得
# with open(CROSS, "U", encoding="utf-8") as fr:
with open(CROSS, "U") as fr:
    next(fr)
    cross_sec = [list(map(float, line.split(","))) for line in fr.read().splitlines()]
    cross_sec = [[Point(*line[1:3]), Point(*line[4:6])] for line in cross_sec  ]

# 各横断の長さを取得
cross_length = [start.distance(end) for start, end in cross_sec]

## 横断方向の単位方向ベクトルを追加
cross_unit = [end.subtract(start) / length for [start, end], length in zip(cross_sec, cross_length)]

## 横断方向との単位法線ベクトルを追加
cross_nunit = [Point(cross.y, -cross.x) for cross in cross_unit]

## 全横断の平均高さを算出
zmean = sum([sum(map(lambda x: x.z, no)) / len(no) for no in xz]) / len(xz)

## シフト用データの取得
modheader=["No.", "bshift", "hshift", "hmag","dummy", "dummy2"]
Mod={}
if os.path.exists(ModBase):
    with open(ModBase, "U", encoding="utf-8", errors="ignore") as fr:
        Mod = [list(map(float, line.split(",")[:4])) for line in fr.read().splitlines()]
        Mod = dict(zip(["No", "bshift", "hshift", "hmag"], list(zip(*Mod))))
else:
    Mod["hmag"] = [1 for i in cross_sec] # 図面上の表示高さの倍率
    Mod["bshift"] = [0 for i in cross_sec]
    Mod["hshift"] = [0 for i in cross_sec]

# Mod["hshift"] = [-zmean for i in cross_sec] # zmeanで平均値を中心にしてもいい
Mod["hshift"] = [0 for i in cross_sec]


xyz = [[] for i in range(len(cross_sec))]
xyh = [[] for i in range(len(cross_sec))]
for cross_idx, [cross, unit, nunit, no] in enumerate(zip(cross_sec, cross_unit, cross_nunit, xz)):
    start = cross[0]
    for pt_idx in range(len(no)):
        if pt_idx is 0: # 基点の位置を指定
            xyz[cross_idx].append(start.add(unit * Mod["bshift"][cross_idx] * DISTANCE_SCALE))
        # 基点を基に残りの点を設定
        distance = (no[pt_idx].x - no[pt_idx -1].x) * DISTANCE_SCALE
        xyz[cross_idx].append(xyz[cross_idx][pt_idx - 1].add(unit * distance))

        xyh[cross_idx].append(xyz[cross_idx][pt_idx].add(nunit * (no[pt_idx].z + Mod["hshift"][cross_idx]) * Mod["hmag"][cross_idx] * DEPTH_SCALE))


## create cross-section.dxf
drawing=ezdxf.new("AC1018") # line_weightの設定のためにR13以上が必要
modelspace=drawing.modelspace()
LAYER="cross-section"
drawing.layers.create(LAYER+"-line", {"color": 5, "line_weight": 30})
drawing.layers.create(LAYER+"-label", {"color": 5})

## 横断線の書き込み
dxfattribs={"layer": LAYER+"-line"}
for cross_idx, [cross_n, cross_s] in enumerate(zip(xyz, xyh)):
    block_name=LAYER+"{:03d}".format(cross_idx+1)
    flag=drawing.blocks.new(name=block_name)
    flag.add_polyline2d(list(map(lambda i: (i.x, i.y), cross_n)), dxfattribs=dxfattribs)
    flag.add_polyline2d(list(map(lambda i: (i.x, i.y), cross_s)), dxfattribs=dxfattribs)
    for pt_n, pt_s in zip(cross_n, cross_s):
        flag.add_polyline2d([[pt_n.x, pt_n.y], [pt_s.x, pt_s.y]], dxfattribs=dxfattribs)
    modelspace.add_blockref(block_name, [0,0], dxfattribs={"layer": LAYER + "-line"})

## 横断ラベルの書き込み
dxfattribs["layer"] = LAYER+"-label"
dxfattribs["height"] = 10 DEPTH_SCALE # 文字の大きさ
for cross_idx, label in enumerate(demheader):
    start = cross_sec[cross_idx][0]
    spos = [start.x -10 * DEPTH_SCALE, start.y -10 * DEPTH_SCALE]
    label = str(cross_idx) + "-" + str(label.split()[0])

    modelspace.add_text(label, dxfattribs=dxfattribs).set_pos(spos, align="RIGHT")
drawing.saveas("check-"+LAYER+".dxf")


## 修正後のBH.dmnを出力
if os.path.exists(ModBase):
    with open("./BH-mod.dmn", "w", newline="\n") as fw:
        for header, no, bshift in zip(demheader, xz, Mod["bshift"]):
            fw.write(header)
            polyline=no
            for pt_idx, pt in enumerate(no, 1):
                xypoint="{xpoint:8.2f}{ypoint:8.2f}".format(xpoint=pt.x + bshift, ypoint=pt.z)
                fw.write(xypoint)
                if pt_idx % 5 == 0 or pt_idx == len(no):
                    fw.write("\n")
