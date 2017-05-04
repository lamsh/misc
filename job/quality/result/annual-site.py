#!/usr/bin/env python3
# coding: utf-8
# (File name: annual-site.py)
# Author: SENOO, Ken
# License: CC0
# (Last update: 2015-03-05T17:53+09:00)

""" ダム貯水池モデルの計算結果から年平均値を出力する
対象項目：
* 水温
* SS
* Chl-a
* COD
* T-N
* T-P
* DO

ダム取水：damflow01など
総放流水：damflow01-04までの合計
ダム表層：site*
"""

import glob

IN_DIR = "./result/"

"""
ダムサイト内
再現計算2009-
"""

site_list = "site_tt.dat site_cod.dat site_dox.dat "

FR = IN_DIR + "site_tt.dat"


def get_surface(filepath, margin=3):
    with open(filepath, "U", encoding="utf-8") as fr:
        val = fr.read().splitlines()

    val[:] = [list(map(float, line.split())) for line in val]
    val[:] = [line[int(line[1]) + margin] for line in val]
    return val


water_temp = get_surface(FR)


FR = IN_DIR + "site_cod.dat"
cod_surface = get_surface(FR)

FR = IN_DIR + "site_dox.dat"
do_surface = get_surface(FR)



## TN
for f_i, fr in enumerate(glob.glob(IN_DIR+"site_*n*.dat")):
    if f_i == 0:
        tn_surface = get_surface(fr)

    tn_surface = [a + b for (a, b) in zip(tn_surface, get_surface(fr))]

## TP
for f_i, fr in enumerate([IN_DIR+"site_pop.dat", IN_DIR+"site_po4.dat"]+glob.glob(IN_DIR+"site_sqp0*.dat")):
    if f_i == 0:
        tp_surface = get_surface(fr)

    tp_surface = [a + b for (a, b) in zip(tp_surface, get_surface(fr))]


## Chl-a
FR = IN_DIR + "site_chla01.dat"
chla_1 = get_surface(FR)

FR = IN_DIR + "site_chla02.dat"
chla_2 = get_surface(FR)

FR = IN_DIR + "site_chla03.dat"
chla_3 = get_surface(FR)

chla_total = [a + b + c for (a, b, c) in zip(chla_1, chla_2, chla_3)]

## SS
FR = IN_DIR + "site_cc.dat"
ss_sand = get_surface(FR)

ss_total = [sand +
        ch_total*0.1840 + ch_1/ch_total*13.5739 + ch_2/ch_total*17.1989 +
        ch_3/ch_total*14.8163 - 10.3716
        for (sand, ch_total, ch_1, ch_2, ch_3) in zip(ss_sand, chla_total, chla_1, chla_2, chla_3)]


FW = "site.csv"
HEADER="water temperature,total SS,sand SS,Chl-a,DO,COD,TN,TP\n"
with open(FW, "w", newline="\n", encoding="utf-8") as fw:
    fw.write(HEADER)
    for (temp, ss_tot, sand, chla, do, cod, tn, tp) in zip(water_temp, ss_total, ss_sand, chla_total, do_surface, cod_surface, tn_surface, tp_surface):
        fw.write(",".join(map(str, (temp, ss_tot, sand, chla, do, cod, tn, tp)))+"\n")
