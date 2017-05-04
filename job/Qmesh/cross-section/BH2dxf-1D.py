#!/usr/bin/env python3
# coding: utf-8
# (File name: BH2dxf-1D.py)
# Author: SENOO, Ken
# (Last update: 2015-01-16T16:49+09:00)
# License: MIT

""" flow
BHd.dmnから横断名を取得してDXFに出力。形状の確認に使う。
"""

import ezdxf
import math

FR="./BH.dmn"

## ファイルから座標とラベル名を抽出
label=[]
with open(FR, "U", encoding="utf-8") as fr: fr=fr.read().splitlines()
cross=[]
cnt=0
while cnt < len(fr):
    label.append(fr[cnt].split()[0])
    npoint=int(fr[cnt].split()[3])
    trow=int(math.ceil(npoint/5.0))
    xy=list(map(float, "".join(fr[cnt+1:cnt+1+trow]).split()))
    cross.append([xy[i:i+2] for i in range(0, len(xy), 2)])
    cnt+=1+trow

nline=len(cross)
FW="./BH.dxf"

wdwg=ezdxf.new()
wdwg.layers.create("BH-line")
wdwg.layers.create("BH-label")
wmds=wdwg.modelspace()

start_x=0
start_y=0
for line in range(nline):
    if (line % 10) == 0: start_x+=300
    wmds.add_polyline2d([(i[0]+start_x, i[1]-100*(line % 10)) for i in cross[line]], dxfattribs={"layer": "BH-line"})
    wmds.add_text(label[line], dxfattribs={"layer": "BH-label", "height": 10}).set_pos([cross[line][0][0]-10+start_x, cross[line][0][1]-100*(line % 10)], align="RIGHT")

wdwg.saveas(FW)
