#!/usr/bin/env python3
# coding: utf-8
# (File name: makeKP.py)
# Author: SENOO, Ken
# (Last update: 2015-01-16T18:51+09:00)
# License: MIT

"""
Tecplotの背景図に使う側線を作るためにDXFを出力
入力：1列目にラベル、2列目以降にcross_sec.csvの内容を貼り付けたKP-river.csv
"""

import ezdxf


FR="./KP-river.csv"

with open(FR, "U", encoding="utf-8") as fr:
    kp = [i.split(",") for i in fr.read().split()]

nkp=len(kp)
kplabel=[i[0] for i in kp]
start=[map(float, i[1:3]) for i in kp]
end=[map(float, i[3:]) for i in kp]


FW="./KP-river.dxf"

wdwg=ezdxf.new()
# wdwg.layers.create("KP-river-line", {"color": 7, "linetype": "dashed"})
wdwg.layers.create("KP-river-line")
wdwg.layers.create("KP-river-label")
wmodelspace=wdwg.modelspace()
# layerにdashedとしても反映されない。linestyleはTecPlotで変える。

for no in range(nkp):
    # wmodelspace.add_polyline2d([start[no], end[no]], dxfattribs={"layer": "KP-river-line", "linetype": "dashed"})
    wmodelspace.add_polyline2d([start[no], end[no]], dxfattribs={"layer": "KP-river-line"})

for no in range(nkp):
    spos=[start[no][0]-50, start[no][1]+20]
    epos=[end[no][0]+50, end[no][1]-20]
    wmodelspace.add_text(kplabel[no], dxfattribs={"layer": "KP-river-label", "height": 10}).set_pos(spos, align="RIGHT")
    wmodelspace.add_text(kplabel[no], dxfattribs={"layer": "KP-river-label", "height": 10}).set_pos(epos)

wdwg.saveas(FW)
