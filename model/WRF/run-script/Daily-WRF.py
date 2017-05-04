#!/usr/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-05-28T10:59+09:00)

import os, sys
import datetime
import subprocess
import glob

START=datetime.datetime(2013,6,1)

START_DATE=datetime.datetime(2013,6,1)
END_DATE=datetime.datetime(2013,6,8)
NOW=START_DATE
DAYS=END_DATE-START_DATE


PWD=os.getcwd()
WPS_DIR=PWD+"/WPS/"
WRF_DIR=PWD+"/WRFV3/run/"


for day in range(DAYS.days):
    NOW=START_DATE+datetime.timedelta(day)
    TOMORROW=NOW+datetime.timedelta(1)
    print(NOW)
    os.chdir(WPS_DIR)
   
    ## geogrid
    if NOW == START:
        print("first date run geogrid")
        os.system("./geogrid.exe > geogrid.log 2>&1")
    
        FR="./namelist.wps.tmpl"
        NAME_DICT={}
        with open(FR) as fr:
            for line in fr:
                if "=" in line:
                   line=line.replace("=","").replace(",","")
                   NAME_DICT.update({line.split()[0]: line.split()[1:]})
        NAME_DICT["parent_id"][0]="0"
        MAX_DOM=map(int, NAME_DICT["max_dom"])[0]

        DX=range(MAX_DOM)
        DY=range(MAX_DOM)

        DX[0]=float(NAME_DICT["dx"][0])
        DY[0]=float(NAME_DICT["dy"][0])
        PARENT_ID=map(int, NAME_DICT["parent_id"])
        PARENT_GRID_RATIO=map(int, NAME_DICT["parent_grid_ratio"])
        
        for domain in range(1,MAX_DOM):
            DX[domain]=DX[PARENT_ID[domain]-1]/PARENT_GRID_RATIO[domain]
            DY[domain]=DY[PARENT_ID[domain]-1]/PARENT_GRID_RATIO[domain]


    os.system("""sed "
            s/(START_DATE)/{DATE1}/g; 
            s/(END_DATE)/{DATE2}/g;
            " namelist.wps.tmpl > namelist.wps""".format(
            DATE1=NOW.isoformat().replace("T","_"),
            DATE2=TOMORROW.isoformat().replace("T","_")
            )
        )

    ## ungrib
    print("ungrib")
    os.system("ln -fs ./ungrib/Variable_Tables/Vtable.GFS Vtable")

    MET_TODAY=os.path.expanduser("~/model/WRF/NCEP-FNL/fnl_{DATE}".format(DATE=NOW.strftime("%Y%m%d")))
    MET_TOMMOROW=os.path.expanduser("~/model/WRF/NCEP-FNL/fnl_{DATE}".format(DATE=TOMORROW.strftime("%Y%m%d_%H_%M")))
    #MET="/home/senooken/model/WRF/NCEP-FNL/fnl_{DATE}*".format(DATE=NOW.strftime("%Y%m%d"))

    os.system("./link_grib.csh {met_today}* {met_tomorrow}".format(met_today=MET_TODAY,
        met_tomorrow=MET_TOMMOROW
        ))
    os.system("./ungrib.exe > ungrib.log 2>&1") # Output for ungrib.exe result.

    ## metgrid
    print("metgrid")
    os.system("./metgrid.exe > metgrid.log 2>&1")

    os.chdir(WRF_DIR)
    
    os.system("ln -fs ../../WPS/met_em* .")

    if NOW == START:
        IS_RESTART = ".false."
    else:
        IS_RESTART = ".true."

    os.system("""sed '
    s/(YEAR1)/{year1}/g;
    s/(MONTH1)/{month1}/g;
    s/(DAY1)/{day1}/g;
    s/(YEAR2)/{year2}/g;
    s/(MONTH2)/{month2}/g;
    s/(DAY2)/{day2}/g;
    s/(IS_RESTART)/{is_start}/;
    s/(MAX_DOM)/{max_dom}/;
    s/(E_WE)/{e_we}/;
    s/(E_SN)/{e_sn}/;
    s/(DX)/{dx}/;
    s/(DY)/{dy}/;
    s/(PARENT_ID)/{parent_id}/;
    s/(I_PARENT_START)/{i_parent_start}/;
    s/(J_PARENT_START)/{j_parent_start}/;
    s/(PARENT_GRID_RATIO)/{parent_grid_ratio}/;
    ' namelist.input.tmpl > namelist.input""".format(
        year1=(str(NOW.year)+", ")*MAX_DOM,
        month1=(str(NOW.month)+", ")*MAX_DOM,
        day1=(str(NOW.day)+", ")*MAX_DOM,
        year2=(str(TOMORROW.year)+", ")*MAX_DOM,
        month2=(str(TOMORROW.month)+", ")*MAX_DOM,
        day2=(str(TOMORROW.day)+", ")*MAX_DOM,
        is_start=IS_RESTART,
        max_dom=", ".join(NAME_DICT["max_dom"]),
        e_we=", ".join(NAME_DICT["e_we"]),
        e_sn=", ".join(NAME_DICT["e_sn"]),
        dx=", ".join(map(str,DX)),
        dy=", ".join(map(str, DY)),
        parent_id=", ".join(NAME_DICT["parent_id"]),
        i_parent_start=", ".join(NAME_DICT["i_parent_start"]),
        j_parent_start=", ".join(NAME_DICT["j_parent_start"]),
        parent_grid_ratio=", ".join(NAME_DICT["parent_grid_ratio"]),
        )
    )
 
    ## save log
    LOGDIR="./log/"
    if not os.path.exists(LOGDIR): os.makedirs(LOGDIR)

    print("real")
    os.system("time mpirun -n 8 ./real.exe > real.log 2>&1" )
    for log in glob.glob("rsl.*"):
        os.rename(log, LOGDIR+"real-"+log+"-{now}".format(now=NOW.strftime("%Y%m%d")))

    print("wrf")
    os.system("time mpirun -n 8 ./wrf.exe > wrf.log 2>&1")
    for log in glob.glob("rsl.*"):
        os.rename(log, LOGDIR+"wrf-"+log+"-{now}".format(now=NOW.strftime("%Y%m%d")))

    os.chdir(PWD)
print("finish")
