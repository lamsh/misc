#!/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken

import netCDF4
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import datetime

def plot_var(X,Y,var):
    BM.drawcoastlines()
    #BM.fillcontinents()
    BM.drawparallels(range(-90,90,1),labels=[1,0,0,0])
    BM.drawmeridians(range(-180,180,1),labels=[0,0,0,1])
    plt.contourf(X,Y,var)
#    plt.pcolormesh(X,Y,var)
    plt.colorbar(pad=0.01, fraction=0.1)
                


ROOTDIR="~/run/20140528_WIND_MTG/"
ROOTDIR=os.path.expanduser(ROOTDIR)
OUTDIR=ROOTDIR+"/fig/"

if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

START_DATE=datetime.datetime(2013,6,1)
END_DATE=datetime.datetime(2013,6,4)
DAYS=END_DATE-START_DATE


VAR_LIST="T2 Q2 TH2 U10 V10 RAINC RAIN"
varlist="Q2 PSFC T2 TH2 U10 V10 RAINC RAINSH RAINNC SNOWNC".split()
## plot configure
plt.ion()
plt.clf()
PARAM={
        "font.size": 12,
        }
plt.rcParams.update(PARAM)


for day in range(DAYS.days):
    NOW=START_DATE+datetime.timedelta(day)
    print(NOW.isoformat())
    INFILE="output/wrfout_d01_{date}_00:00:00".format(date=NOW.strftime("%Y-%m-%d"))
    MODEL_NC=netCDF4.Dataset(ROOTDIR+INFILE)

    if day == 0:

        ## get projection information
        XCENT=MODEL_NC.CEN_LON
        YCENT=MODEL_NC.CEN_LAT

        DX=MODEL_NC.DX
        DY=MODEL_NC.DY

        P_ALP=MODEL_NC.TRUELAT1
        P_BET=MODEL_NC.TRUELAT2

        NCOLS=MODEL_NC.getncattr("WEST-EAST_PATCH_END_UNSTAG")
        NROWS=MODEL_NC.getncattr("SOUTH-NORTH_PATCH_END_UNSTAG")

        ## basemap
        BM=Basemap(resolution="f", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

        MESH_PROJ_X,MESH_PROJ_Y=BM(MODEL_NC.variables["XLONG"][0],MODEL_NC.variables["XLAT"][0])


## plt.plot(PROJ_X,PROJ_Y,"o") # test
#plt.pcolormesh(MESH_PROJ_X,MESH_PROJ_Y,MODEL_NC.variables["T2"][0])
#plt.colorbar(fraction=0.1,pad=0.01)


#plt.savefig(OUTDIR+"T2.png",bbox_inches="tight")

    plt.clf()
    plot_var(MESH_PROJ_X, MESH_PROJ_Y, 
            np.mean(
                np.dstack(MODEL_NC.variables["T2"][:-1]-273.15),
                    axis=2,dtype=np.float128
                )
            )
    plt.title("Daily surface Temperature on {date}".format(date=NOW.strftime("%Y-%m-%d")))
    plt.figtext(0.8,0.92,"[{unit}]".format(unit="$^o$C",size=14))
    OUTIFLE="daily_T2_{date}".format(date=NOW.strftime("%Y%m%d"))
    plt.savefig(OUTDIR+OUTIFLE+".png", bbox_inches="tight")
    plt.savefig(OUTDIR+OUTIFLE+".pdf", bbox_inches="tight")

    plt.clf()
    plot_var(MESH_PROJ_X, MESH_PROJ_Y, 
            np.mean(
                np.dstack(MODEL_NC.variables["PSFC"][:-1]/100),
                    axis=2,dtype=np.float128
                )
            )

    plt.title("Daily surface Pressure on {date}".format(date=NOW.strftime("%Y-%m-%d")))
    plt.figtext(0.8,0.92,"[{unit}]".format(unit="hPa",size=14))
    OUTIFLE="daily_PSFC_{date}".format(date=NOW.strftime("%Y%m%d"))
    plt.savefig(OUTDIR+OUTIFLE+".png", bbox_inches="tight")
    plt.savefig(OUTDIR+OUTIFLE+".pdf", bbox_inches="tight")

    plt.clf()
    BM.drawcoastlines()
    #BM.fillcontinents()
    BM.drawparallels(range(-90,90,1),labels=[1,0,0,0])
    BM.drawmeridians(range(-180,180,1),labels=[0,0,0,1])


    MU10=np.mean(np.dstack(MODEL_NC.variables["U10"][:-1]), axis=2, dtype=np.float128)
    MV10=np.mean(np.dstack(MODEL_NC.variables["V10"][:-1]), axis=2, dtype=np.float128)

    plt.contourf(MESH_PROJ_X, MESH_PROJ_Y, np.sqrt(MU10**2+MV10**2))
    plt.colorbar(pad=0.01, fraction=0.1)
    plt.quiver(MESH_PROJ_X, MESH_PROJ_Y, MU10, MV10, linewidth = 1, angles="uv", edgecolor="None")


    plt.title("Daily surface Wind on {date}".format(date=NOW.strftime("%Y-%m-%d")))
    plt.figtext(0.8,0.92,"[{unit}]".format(unit="m/s",size=14))
    OUTIFLE="daily_UV10_{date}".format(date=NOW.strftime("%Y%m%d"))
    plt.savefig(OUTDIR+OUTIFLE+".png", bbox_inches="tight")
    plt.savefig(OUTDIR+OUTIFLE+".pdf", bbox_inches="tight")
