#!/bin/env python2.7
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os, sys

## open position information file
#fr="/home/senoo/skydrive/document/run/EA.1201-1303/observation/pol/pol_pos_hirohara.csv"
fr="/home/senoo/skydrive/document/run/EA.1201-1303/observation/met/pos_met.csv"
pos_array=np.genfromtxt(fr,delimiter=",",names=True,dtype=None)

## automatically get lattitude laongitude column header from character  "lat", "lon".
## automatically get position column header  from character "loc" or "cit" or "cap".
LON_LABEL="".join(filter(lambda x: "lon" in x.lower(), pos_array.dtype.names))
LAT_LABEL="".join(filter(lambda x: "lat" in x.lower(), pos_array.dtype.names))
POS_LABEL="".join(filter(lambda x: "loc" in x.lower() or "cit" in x.lower() or  "cap" in x.lower(), pos_array.dtype.names))
## get array of longitude, latitude, position name.
pos_lon=pos_array[LON_LABEL]
pos_lat=pos_array[LAT_LABEL]
pos_city=pos_array[POS_LABEL]
markers="o p d D < > ^ v p s d D * d x 6 7".split()

TITLE_OBS="Observation Position"
FSLATLON=14


# ave = (np.max(pos_lon) - np.min(pos_lon))/2.0
# ave = (np.max(pos_lat) - np.min(pos_lat))/2.0

""" 自動化の手順 not complete
1. 中心位置を取得
2. 中心位置を中心に4領域に区分
3. それぞれの領域に
. どこに余白が多いかを探す
"""
#pos_lat

# clear previous figure 
plt.clf()

#m = Basemap(projection="ortho",lat_0=45, lon_0=10)

## for japan
m = Basemap(projection="merc",resolution="i",llcrnrlat=31, llcrnrlon=126, urcrnrlat=45, urcrnrlon=144)
## for East Asia
#m = Basemap(projection="merc",resolution="i",llcrnrlat=-10, llcrnrlon=-70, urcrnrlat=50, urcrnrlon=150)

m.drawcoastlines()
m.drawcountries()
#m.fillcontinents(lake_color="aqua",color=(1,0.8,1))
#m.fillcontinents(color=(0.9,1,.9))
m.fillcontinents(color=(0.9,0.9,0.9))
#m.drawmapboundary(fill_color="aqua")
m.drawmapboundary()

m.drawparallels(range(-90, 90, 2), labels = [1,0,0,0], fontsize=FSLATLON)
m.drawmeridians(range(-180, 180, 5), labels = [0,0,0,1], fontsize=FSLATLON)

## convert 1-D list of position  to 2-D mesh
base_lon,base_lat=m(pos_lon,pos_lat)

for i, city in enumerate(range(len(pos_array))):
    plt.plot(base_lon[i], base_lat[i], c=plt.cm.rainbow(i*290/len(pos_array)),marker=markers[i],label=pos_city[i], alpha=1, ms=8)

#plt.legend(loc="lower left")
plt.legend(loc="upper left")

## plot result point
#for city, xc, yc in zip(cities, x, y):
#    plt.text(xc+30000, yc-150000, city, bbox=dict(facecolor="white", alpha=1.0), size="small")

#plt.title(TITLE_OBS,size=14)


## plot station
#==============================================================================
# x,y=m(olon, olat)
# m.plot(x,y,c=(1,0.8,1),ls="", marker="o", ms =10)
# for city, xc, yc in zip(ostation, x, y):
#     plt.text(xc+xc/10, yc, city, bbox=dict(facecolor="white", alpha=1))
# 
# plt.title("Station and calculation position", fontsize=20)
#==============================================================================
i
fw="./fig/"
if not os.path.exists(fw): os.makedirs(fw)

plt.savefig(fw+"station-position.png",bbox_inches="tight")
plt.savefig(fw+"station-position.pdf",bbox_inches="tight")
