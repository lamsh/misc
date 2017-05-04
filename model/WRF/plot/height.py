#!/bin/env python2.7
# coding: utf-8
# @author: SENOO Ken

"""
This program is make  distribution map from WPS geogrid geo_em.d0?.nc.
"""

import netCDF4
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os

fr="/usr602/senoo/run/EA.1201-1303/wrf/geo_em.d01.nc"
geo_nc=netCDF4.Dataset(fr)

save_dir="./fig/wrf/"
if not os.path.exists(save_dir): os.makedirs(save_dir)

## get projection parameter
DX,DY=geo_nc.DX, geo_nc.DY
XCENT,YCENT=geo_nc.CEN_LON, geo_nc.CEN_LAT
P_ALP,P_BET=geo_nc.TRUELAT1, geo_nc.TRUELAT2
NCOLS,NROWS=geo_nc.__getattribute__( "WEST-EAST_PATCH_END_UNSTAG" ), geo_nc.__getattribute__("SOUTH-NORTH_PATCH_END_UNSTAG")

plt.ion()
plt.clf()
print("make Basemap object")
m = Basemap(resolution="l", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

## x y coordinate
XORIG,YORIG=m(geo_nc.corner_lons[0],geo_nc.corner_lats[0])
lcc_x=[XORIG+DX*j for j in range(NCOLS)]
lcc_y=[YORIG+DY*i for i in range(NROWS)]
mesh_lcc_x,mesh_lcc_y=np.meshgrid(lcc_x,lcc_y)

latlon_fs=16

#varlist_mcip=["LU_INDEX"]
varlist_mcip=["HGT_M"]
for var in varlist_mcip:
    plt.clf()
    m.drawcoastlines(color="k",linewidth=0.5); m.drawcountries(color="k",linewidth=0.6)
    m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], fontsize=latlon_fs)
    m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
    plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,
#    plt.contourf(mesh_lcc_x, mesh_lcc_y,
            geo_nc.variables[var][0,:],
            cmap=plt.cm.jet,
            #levels=range(geo_nc.NUM_LAND_CAT)
            )
    plt.colorbar(pad=0.01,fraction=0.1)
#    plt.colorbar(pad=0.01,fraction=0.1,ticks=range(geo_nc.NUM_LAND_CAT+1)).set_ticklabels(range(1,geo_nc.NUM_LAND_CAT+1))
#    plt.clim(1,24)
    title="Toporography Height [m MSL]"
    plt.title(title,size=20)
#    plt.figtext(0.8,0.91,"[{unit}]".format(unit=geo_nc.variables[var].units.strip()),size=14)
    fw="height"
    plt.savefig(save_dir+fw+".png",bbox_inches="tight") 
#    plt.savefig(save_dir+fw+".pdf",bbox_inches="tight") 
