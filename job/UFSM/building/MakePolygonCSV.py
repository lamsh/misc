#!/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-08-08T10:48+09:00)

## this program convert QGIS output converted lat lon file to polygon.csv.

"""
output format
iBLDG   OBJECTID    ALL_ID  iBT Z_Floor Floor   xx  yy
1   1   20B13   1   233.45  2   -19644.96   -28445.79

* 反時計回りに番号を付ける。

----------------------------
列  項目    説明
----------------------------
A   iBLDG   建物番号
B   OBJECTID    ID。
C   ALL_ID  GISの建物ID？。プログラムでは不使用。
D   iBT 建物種類。1:木造，2:防火木造，3:鉄骨造，4:RC造，5:非木造，6:車庫。
E   Z_Floor z座標(標高)
F   Floor   建物階数
G   xx  x座標
H   yy  y座標
----------------------------
XYには一周できるように最初の座標も必要。
"""

import numpy as np
import os, sys

INDIR="E:/cygwin/home/senooken/senooken/run/UFSM/Saitama-shi_Nishi-ku/"
INFILE="SaitamaWestBuilding.gmt"
OUTDIR="./"
if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

FR=INDIR+INFILE
FW=OUTDIR+"./polygon.csv"
if os.path.exists(FW): os.remove(FW)

BNUM=1 # building number
XY=[]
FMT="%i,%i,%i,%i,%-5.2f,%i,%16.9f,%16.9f,%16.9f"

## 建物種別は"基盤地図情報ダウンロードデータファイル仕様書"を参照。
## 定義は"公 共 測 量 標 準 図 式"を参照。
BUILDING_MAP={
        "普通建物": 1,
        "堅ろう建物":2,
        "普通無壁舎":1,
        "堅ろう無壁舎":2,
        "その他":1,
        "不明":1,
        }

## 建物の階数。建物種別から判別。
FLOOR_TYPE={
        "普通建物": 2,
        "堅ろう建物":3,
        "普通無壁舎":2,
        "堅ろう無壁舎":3,
        "その他":1,
        "不明":1,
        }

HEADER=",".join("iBLDG   OBJECTID    ALL_ID  iBT Z_Floor[m] Floor   xx[m]  yy[m] AREA[m²]".split())+"\n"
NODEID=1

"""
* 先頭の値が数値か-であるときは連続してX, Yの値を取得。
* #が出てきた取得したX, Yの配列を整形して出力。

"""



"""
建物種別があればその属性と標高を取得

次の行へ行き、座標値を取得する
行頭が>になったら座標値取得をやめファイルへ出力


"""
with open(FR) as fr, open(FW,"awb") as fw:
    fw.write(HEADER)
    for line in fr:
        if line.startswith("#") and 1 < len(set([line.find(i) for i in BUILDING_MAP.keys()])):  # 建物種別のどれかがあるときだけ以下を実行
            # print(line)
            BUILDING_TYPE=line.rstrip().split("|")[-3]
            DEM=float(line.rstrip().split("|")[-1])
            
        if line[0].isdigit() or line[0] == "-": 
            XY.append(line.split())

        if line.startswith(">"):
            iBT=np.array([BUILDING_MAP[BUILDING_TYPE] for i in range(len(XY))])
            OBJECTID=np.arange(NODEID,NODEID+len(XY))
            NBUILDING=np.array([BNUM-1 for i in range(len(XY))])
            Z=np.array([DEM for i in range(len(XY))])
            FLOOR=np.array([FLOOR_TYPE[BUILDING_TYPE] for i in range(len(XY))])
            # SUMNODE=np.array( [len(XY) for i in range(len(XY))]) # total node
            # NNODE=np.arange(1,len(XY)+1) # node number
            OUTARRAY=np.column_stack([NBUILDING, OBJECTID, np.arange(len(XY)), iBT, Z,FLOOR])
            # if BNUM==2: sys.exit()

            if BNUM!=1:
                ## 外積により符号付きポリゴン面積を算出。面積が-であれば右手座標系で反時計回りの番号付けとなっているので並び替える。
                ## 修正。樋本先生のpolygon.csvでは時計回りになっていたのでこれに合わせる
                XY=np.array(XY,dtype=np.float64)
                AREA=np.sum([np.cross(XY[i],XY[i+1]) for i in range(len(XY)-1)])/2.0 

                if AREA > 0: 
                    #print("Detect inverse node order. Sort")
                    XY=XY[::-1]

                ## 面積が1 m²以上の建物だけファイルに出力。
                if abs(AREA) >= 1: 
                    OUTARRAY=np.hstack([OUTARRAY,np.array(XY,dtype=np.float64)])
                    OUTARRAY=np.column_stack([OUTARRAY, np.repeat(abs(AREA), len(XY))])
                    np.savetxt(fw, OUTARRAY,fmt=FMT)
                else:
                    NODEID-=len(XY)
                    BNUM-=1
                    OBJECTID-=1
            
            NODEID+=len(XY)
            XY=[]
            BNUM+=1
            OBJECTID+=1
