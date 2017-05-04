#!/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken

import netCDF4
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os

INDIR="/home/senooken/model/WRF/WRF-3.6-single/WRFV3/run/"
INFILE="wrfout_d01_2013-06-01_00:00:00"
FR=INDIR+INFILE
OUTDIR="./fig/"

if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

MODEL_NC=netCDF4.Dataset(FR)

# MODEL_NC.ncattrs() # all attributes list

## get projection information
XCENT=MODEL_NC.CEN_LON
YCENT=MODEL_NC.getncattr("CEN_LAT")

DX=MODEL_NC.DX
DY=MODEL_NC.DY

P_ALP=MODEL_NC.TRUELAT1
P_BET=MODEL_NC.TRUELAT2

NCOLS=MODEL_NC.__getattr__("WEST-EAST_PATCH_END_UNSTAG")
NROWS=MODEL_NC.__getattribute__("SOUTH-NORTH_PATCH_END_UNSTAG")

## basemap
bm=Basemap(resolution="l", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

bm.drawcoastlines()
#bm.fillcontinents()
bm.drawparallels(range(-90,90,10),labels=[1,0,0,0])
bm.drawmeridians(range(-180,180,10),labels=[0,0,01])

## XLAT, XLONG

MODEL_NC.variables["XLAT"][0]
MODEL_NC.variables["XLONG"][0]

#bm(MODEL_NC.variables["XLAT"][0], MODEL_NC.variables["XLONG"][0])

# Y0=MODEL_NC.variables["XLAT"][0,0,0]
# X0=MODEL_NC.variables["XLONG"][0,0,0]
# 
# XORIG,YORIG=bm(X0,Y0)
# PROJ_X=[XORIG+DX*j for j in range(NCOLS)]
# PROJ_Y=[YORIG+DY*i for i in range(NROWS)]
# MESH_PROJ_X,MESH_PROJ_Y=np.meshgrid(PROJ_X,PROJ_Y)

MESH_PROJ_X,MESH_PROJ_Y=bm(MODEL_NC.variables["XLONG"][0],MODEL_NC.variables["XLAT"][0])
## plt.plot(PROJ_X,PROJ_Y,"o") # test
plt.pcolormesh(MESH_PROJ_X,MESH_PROJ_Y,MODEL_NC.variables["T2"][0])
plt.colorbar(fraction=0.1,pad=0.01)

plt.savefig(OUTDIR+"T2.png",bbox_inches="tight")



px,py=bm(135,30)
int(round((px/DX-1)))

