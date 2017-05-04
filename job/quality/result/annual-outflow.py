#!/usr/bin/env python3
# coding: utf-8
# (File name: annual-outflow.py)
# Author: SENOO, Ken
# License: CC0
# (Last update: 2015-03-10T17:41+09:00)


"""表層のダム放流水質を集計
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

流量で加重平均する

"""

import glob
import csv

IN_DIR = "./result/"


def get_variable(filepath):
    with open(filepath) as fr:
        header = next(fr).split()
        val = list(csv.DictReader(fr, delimiter=" ", skipinitialspace=True, quoting=csv.QUOTE_NONNUMERIC, fieldnames=header))
    return val


## 水温、SS
q_out =[]
temp_out = []
ss_sand = []

for f_i, fr in enumerate(glob.glob(IN_DIR+"damflow0*.dat")):
    dam_fr = get_variable(fr)

    if f_i == 0:
        for line_i, line in enumerate(dam_fr):
            q = line["qout"]
            temp_out.append(q * line["tout"])
            ss_sand.append(q * line["cout00"])
            q_out.append(q)

    for line_i, line in enumerate(dam_fr):
        q = line["qout"]
        temp_out[line_i] += q * line["tout"]
        ss_sand[line_i] += q * line["cout00"]
        q_out[line_i] += q

for line_i in range(len(q_out)):
    temp_out[line_i] /= q_out[line_i]
    ss_sand[line_i] /= q_out[line_i]


## Chl-a
q_out[:] = []
chla1_out = []
chla2_out = []
chla3_out = []

for f_i, fr in enumerate(glob.glob(IN_DIR+"damflowp0*.dat")):
    dam_fr = get_variable(fr)

    if f_i == 0:
        for line in dam_fr:
            q = line["qout"]
            chla1_out.append(q * line["chla01"])
            chla2_out.append(q * line["chla02"])
            chla3_out.append(q * line["chla03"])
            q_out.append(q)

    for line_i, line in enumerate(dam_fr):
        q = line["qout"]
        chla1_out[line_i] += q * line["chla01"]
        chla2_out[line_i] += q * line["chla02"]
        chla3_out[line_i] += q * line["chla03"]
        q_out[line_i] += q

for line_i in range(len(q_out)):
    chla1_out[line_i] /= q_out[line_i]
    chla2_out[line_i] /= q_out[line_i]
    chla3_out[line_i] /= q_out[line_i]

chla_total = [a + b + c for (a, b, c) in zip(chla1_out, chla2_out, chla3_out)]

ss_total = [sand +
        ch_total*0.1840 + ch_1/ch_total*13.5739 + ch_2/ch_total*17.1989 +
        ch_3/ch_total*14.8163 - 10.3716
        for (sand, ch_total, ch_1, ch_2, ch_3) in zip(ss_sand, chla_total, chla1_out, chla2_out, chla3_out)]

## 水質
### DO, COD
q_out[:] = []
do_out = []
cod_out = []

for f_i, fr in enumerate(glob.glob(IN_DIR+"damflows0*.dat")):
    dam_fr = get_variable(fr)

    if f_i == 0:
        for line in dam_fr:
            q = line["qout"]
            do_out.append(q * line["dox"])
            cod_out.append(q * line["cod"])
            q_out.append(q)

    for line_i, line in enumerate(dam_fr):
        q = line["qout"]
        do_out[line_i] += q * line["dox"]
        cod_out[line_i] += q * line["cod"]
        q_out[line_i] += q

for line_i in range(len(q_out)):
    do_out[line_i] /= q_out[line_i]
    cod_out[line_i] /= q_out[line_i]


### TN, TP
q_out[:] = []
tp_out = []
tn_out = []

for f_i, (fr_s, fr_p) in enumerate(zip(glob.glob(IN_DIR+"damflows0*.dat"), glob.glob(IN_DIR+"damflowp0*.dat"))):
    dam_fr_s = get_variable(fr_s)
    dam_fr_p = get_variable(fr_p)

    if f_i == 0:
        for line_s, line_p in zip(dam_fr_s, dam_fr_p):
            q = line_s["qout"]
            tp_out.append(q * (
                line_s["pop"]+line_s["po4"]+line_s["p_po4"] +
                line_p["sqp01"]+line_p["sqp02"]+line_p["sqp03"]
                ))
            tn_out.append(q * (
                line_s["pon"]+line_s["nh4"]+line_s["no2"]+line_s["no3"] +
                line_p["sqn01"]+line_p["sqn02"]+line_p["sqn03"]
                ))
            q_out.append(q)

    for line_i, (line_s, line_p) in enumerate(zip(dam_fr_s, dam_fr_p)):
        q = line_s["qout"]
        tp_out[line_i] += q * (
                line_s["pop"]+line_s["po4"]+line_s["p_po4"] +
                line_p["sqp01"]+line_p["sqp02"]+line_p["sqp03"]
                )
        tn_out[line_i] += q * (
                line_s["pon"]+line_s["nh4"]+line_s["no2"]+line_s["no3"] +
                line_p["sqn01"]+line_p["sqn02"]+line_p["sqn03"]
                )
        q_out[line_i] += q

for line_i in range(len(q_out)):
    tn_out[line_i] /= q_out[line_i]
    tp_out[line_i] /= q_out[line_i]


FW = "dam.csv"
HEADER="water temperature,total SS,sand SS,Chl-a,DO,COD,TN,TP\n"
with open(FW, "w", newline="\n", encoding="utf-8") as fw:
    fw.write(HEADER)
    for (temp, ss_tot, sand, chla, do, cod, tn, tp) in zip(temp_out, ss_total, ss_sand, chla_total, do_out, cod_out, tn_out, tp_out):
        fw.write(",".join(map(str, (temp, ss_tot, sand, chla, do, cod, tn, tp)))+"\n")
