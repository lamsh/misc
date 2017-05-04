#!/ur/bin/env python2.7
# -*- coding: utf-8 -*-
# @author: SENOO, Ken
# (Last Update: 2014-05-26T19:42+09:00)

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys

def draw_screen_poly( lats, lons):
    x, y =  lons, lats 
    xy = zip(x,y)
    poly = plt.Polygon( xy, edgecolor="b",fc="none", lw=2, alpha=1)
    plt.gca().add_patch(poly)

# clear previous figure 
plt.ion()
plt.clf()

## setting namelist.wps domain information
INDIR="/home/senooken/model/WRF/WRF-3.6/WPS/"
INFILE="namelist.wps.tmpl"
FR=INDIR+INFILE
NAME_DICT={}
with open(FR) as fr:
    for line in fr:
        if "=" in line:
           line=line.replace("=","").replace(",","")
           NAME_DICT.update({line.split()[0]: line.split()[1:]})



DX = float(NAME_DICT["dx"][0])
DY = float(NAME_DICT["dy"][0])

MAX_DOM = int(NAME_DICT["max_dom"][0])

PARENT_GRID_RATIO = map(int, NAME_DICT["parent_grid_ratio"])

I_PARENT_START = map(int, NAME_DICT["i_parent_start"])
J_PARENT_START = map(int, NAME_DICT["j_parent_start"])

E_SN = map(int, NAME_DICT["e_sn"])
E_WE = map(int, NAME_DICT["e_we"])

REF_LAT=  float(NAME_DICT["ref_lat"][0])
REF_LON=  float(NAME_DICT["ref_lon"][0])

TRUELAT1 = float(NAME_DICT["truelat1"][0])
TRUELAT2 = float(NAME_DICT["truelat2"][0])

## draw map
BM = Basemap(resolution="f", projection="lcc", rsphere=(6370000.0, 6370000.0), 
lat_1=TRUELAT1, lat_2=TRUELAT2, lat_0=REF_LAT, lon_0=REF_LON, 
width=DX*(E_WE[0]-1), height=DY*(E_SN[0]-1))

BM.drawcoastlines()
#m.drawcountries(linewidth=2)
BM.drawcountries()

#m.fillcontinents()
BM.fillcontinents(color=(0.8,1,0.8))
BM.drawmapboundary()
#m.fillcontinents(lake_color="aqua")
#m.drawmapboundary(fill_color="aqua")

BM.drawparallels(np.arange(-90, 90, 0.1), labels = [1,0,0,0], fontsize=16,dashes=[1,1])
BM.drawmeridians(np.arange(-180, 180, 0.1), labels = [0,0,0,1], fontsize=16,dashes=[1,1])


## plot center position
cenlon=range(MAX_DOM); cenlat=range(MAX_DOM)
cenlon_model=DX*(E_WE[0]-1)/2.0
cenlat_model=DY*(E_SN[0]-1)/2.0

cenlon[0], cenlat[0]=BM(cenlon_model, cenlat_model, inverse=True)

#plt.plot(cenlon,cenlat,marker="o",color="gray")
plt.plot(cenlon_model,cenlat_model, marker="o", color="gray")
plt.text(cenlon_model*1.01, cenlat_model*1.01, "({cenlon}, {cenlat})".format(
    cenlon=round(cenlon[0],2), cenlat=round(cenlat[0],2))
        )
#print cenlon, cenlat

#### draw nested domain rectangle
lon=range(4); lat=range(4)

if MAX_DOM >= 2:
    ### domain 2
    # 4 corners
    ll_lon = DX*(I_PARENT_START[1]-1)
    ll_lat = DY*(J_PARENT_START[1]-1)
    ur_lon = ll_lon + DX/PARENT_GRID_RATIO[1] * (E_WE[1]-1)
    ur_lat = ll_lat + DY/PARENT_GRID_RATIO[1] * (E_SN[1]-1)
    
    ## lower left (ll)
    lon[0],lat[0] = ll_lon, ll_lat
    ## lower right (lr)
    lon[1],lat[1] = ur_lon, ll_lat
    ## upper right (ur)
    lon[2],lat[2] = ur_lon, ur_lat
    ## upper left (ul)
    lon[3],lat[3] = ll_lon, ur_lat
    
    draw_screen_poly(lat, lon)
    #plt.scatter(lon,lat)
    plt.plot(lon, lat, "o")
#    plt.text(lon[0]*0.9, lat[0]*0.9, "({i}, {j})".format(i=I_PARENT_START[1], j=J_PARENT_START[1]))
#    for node in range(4):
#        plt.text(lon[node],lat[node],"({i}, {j})".format(i=I_PARENT_START[1], j=J_PARENT_START[1]))
#
    cenlon_model = ll_lon + (ur_lon-ll_lon)/2.0
    cenlat_model = ll_lat + (ur_lat-ll_lat)/2.0
    cenlon[1], cenlat[1]=BM(cenlon_model, cenlat_model, inverse=True)

#    plt.plot(cenlon_model, cenlat_model,marker="o")
    
    #print m(cenlon, cenlat)cenlon, cenlat, ll_lon, ll_lat, ur_lon, ur_lat
    #print m(cenlon, cenlat,inverse=True)


if MAX_DOM >= 3:
    ### domain 3
    ## 4 corners
    ll_lon += DX/PARENT_GRID_RATIO[1]*(I_PARENT_START[2]-1)
    ll_lat += DY/PARENT_GRID_RATIO[1]*(J_PARENT_START[2]-1)
    ur_lon = ll_lon +DX/PARENT_GRID_RATIO[1]/PARENT_GRID_RATIO[2]*(E_WE[2]-1)
    ur_lat =ll_lat+ DY/PARENT_GRID_RATIO[1]/PARENT_GRID_RATIO[2]*(E_SN[2]-1)
    
    ## ll
    lon[0],lat[0] = ll_lon, ll_lat
    ## lr
    lon[1],lat[1] = ur_lon, ll_lat
    ## ur
    lon[2],lat[2] = ur_lon, ur_lat
    ## ul
    lon[3],lat[3] = ll_lon, ur_lat
    
    draw_screen_poly(lat, lon)
    plt.text(lon[0]-lon[0]/10,lat[0]-lat[0]/10,"({i}, {j})".format(i=I_PARENT_START[2], j=J_PARENT_START[2]))
    #plt.plot(lon,lat,linestyle="",marker="o",ms=10)

    cenlon_model = ll_lon + (ur_lon-ll_lon)/2.0
    cenlat_model = ll_lat + (ur_lat-ll_lat)/2.0
#    plt.plot(cenlon,cenlat,marker="o",ms=15)
    #print m(cenlon, cenlat)cenlon, cenlat, ll_lon, ll_lat, ur_lon, ur_lat
    #print m(cenlon, cenlat,inverse=True)
    cenlon[2], cenlat[2]=BM(cenlon_model, cenlat_model, inverse=True)


if MAX_DOM >= 4:
    ### domain 3
    ## 4 corners
    ll_lon += DX/PARENT_GRID_RATIO[1]/PARENT_GRID_RATIO[2]*(I_PARENT_START[3]-1)
    ll_lat += DY/PARENT_GRID_RATIO[1]/PARENT_GRID_RATIO[2]*(J_PARENT_START[3]-1)
    ur_lon = ll_lon +DX/PARENT_GRID_RATIO[1]/PARENT_GRID_RATIO[2]/PARENT_GRID_RATIO[3]*(E_WE[3]-1)
    ur_lat =ll_lat+ DY/PARENT_GRID_RATIO[1]/PARENT_GRID_RATIO[2]/PARENT_GRID_RATIO[3]*(E_SN[3]-1)
    
    ## ll
    lon[0],lat[0] = ll_lon, ll_lat
    ## lr
    lon[1],lat[1] = ur_lon, ll_lat
    ## ur
    lon[2],lat[2] = ur_lon, ur_lat
    ## ul
    lon[3],lat[3] = ll_lon, ur_lat
    
    draw_screen_poly(lat, lon)
    #plt.plot(lon,lat,linestyle="",marker="o",ms=10)

    cenlon_model = ll_lon + (ur_lon-ll_lon)/2.0
    cenlat_model = ll_lat + (ur_lat-ll_lat)/2.0
#    plt.plot(cenlon,cenlat,marker="o",ms=15)
    #print m(cenlon, cenlat)cenlon, cenlat, ll_lon, ll_lat, ur_lon, ur_lat
    #print m(cenlon, cenlat,inverse=True)
    cenlon[3], cenlat[3]=BM(cenlon_model, cenlat_model, inverse=True)


with open("/home/senooken/run/20140528_WIND_MTG/observation-position-d2.csv") as f:
    f.next()
    for line in f:
        X,Y=BM(*map(float, line.strip().split(",")[1:]))
        LABEL=line.strip().split(",")[0]
        plt.plot(X,Y,"o",label=LABEL)
#        print(line)

plt.legend(loc="best")
plt.title("Domain and AMeDAS Observation",size=18)
#plt.plot(133.1017)

## save domain by pdf and png
plt.savefig("domain-test.pdf", bbox_inches="tight",edgecolor="none")
plt.savefig("domain-test.png", bbox_inches="tight", edgecolor="none")

# print each domain center lon lat
for i in range(MAX_DOM):
    print cenlon[i], cenlat[i]


