#!/usr/bin/env python2.7
# coding: utf-8
# (File name: extract-htable.py)
# Author: SENOO, Ken
# (Last update: 2014-09-29T10:13+09:00)
# License: MIT


"""
帳票形式の水位データから値を取得して日付をつけた2列のcsvとして出力
"""

import xlrd
import glob
import datetime
import calendar

INDIR="/cygdrive/f/Users/senooken/work/14A10_ZIZOUGAWA/work/20140919_QuantityGraph/1_mk_qt/基データ/"
FW="./inter.csv"

START_ROW=5
START_COL=2

with open(FW, "wb") as fw: # writer header
    fw.writelines("datetime,height[m]\n")

SYEAR=1997
LYEAR=2014
idate=datetime.datetime(SYEAR, 1, 1, 1)

for year in range(SYEAR, LYEAR+1):
    print(year)
    FR=glob.glob(INDIR+str(year)+"*")[0]
    wb=xlrd.open_workbook(FR)
    sheet_name=wb.sheet_names()
    value=[]

    # 対象シートの年月から日数を算出して、シート範囲を一括して値を取得
    # xlrdはセルの他に行ごとか列ごとにしか範囲指定できない
    for month, sheet in enumerate(sheet_name, 1):
        ws=wb.sheet_by_name(sheet)
        monthdays=calendar.monthrange(year, month)[1]
        for day in range(monthdays):
            value.append(ws.col_values(START_COL+day, START_ROW, START_ROW+24))

    isodate="{date.year}-{date.month:02d}-{date.day:02d}T{date.hour:02d}:00"
    days= 366 if calendar.isleap(year) else 365
    dtime=[isodate.format(date=datetime.datetime(year, 1, 1, 1)+ datetime.timedelta(hours=i)) for i in range(days*24)]

    value=[j for i in value for j in i] # flatten

    with open(FW, "awb") as fw:
         fw.writelines("\n".join([dtime[i]+","+str(value[i]) for i in range(len(value))])+"\n")
