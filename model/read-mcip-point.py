#!/bin/env python2.7
# coding: utf-8
# @author: SENOO Ken

"""
== Description
 * This program extract surface hourly point data from CCTM output file.
 * And plot observation position in model domain.
 * This program needs time. 3 positions and  1 day and SAPRC-99 mechanism is required 40 seconds.

== Program flow
 * get observation position data from file
 * convert observation lat-lon to model lcc and col row
 * save file for hourly all species with header including position name, lat, lon, col , row,unit

== Need
 * Output file position (specified by FW variable)
 * GRIDDESC file (specified by GRIDFILE variable)
 * Model output file (specified by MODEL_FILE variable)
 * observation information file (specified by POS_FILE variable), format is below.
-------------------------------
location, latitiude, longitude
-------------------------------
Japan, 30, 135
China, 40, 100
--------------------------------

In observation information file, header(first row) is required. But order is ignored.
This program is recognized in header charecter includeing "lat"=latitude, "lon"=longitude, "loc" or "cit" or "pos" = location. In header, character case is ignored for this program. Also you can specify your any column by manual.
"""

#from scipy.io import netcdf
import netCDF4
import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import numpy as np
import os
import sys


## set save directory
model_type="mcip"
APPL="CJ.201301-201303" # model run name
#APPL="IN.1306" # model run name
DOM="D1"
root_dir="/usr601/senoo/run/"+APPL # model output root directory
#root_dir="/home/kuramoto/run/"+APPL # model output root directory
root_save_dir="./fig/" # root save directory
model_save_dir=root_save_dir+"/{0}/pol_pos/".format(model_type)
mech="saprc-99"#cb05
#mech="cb05"
is_megan="with_megan"
is_mozart="with_mozart"

## open file
#mydata="{dir}/{type}/{mech}/{is_megan}/{mozart}".format(type=model_type,mech=mech,is_megan=is_megan,dir=root_dir,mozart=is_mozart)
mydata="{dir}/{model}/".format(dir=root_dir,model=model_type)

## set date
(styear,stmonth,stday,sthour) = (2012,12,31,0)
(enyear,enmonth,enday,enhour) = (2013,4,2,0)

stime0=datetime.datetime(styear,stmonth,stday,sthour)
etime0=datetime.datetime(enyear,enmonth,enday,sthour)

## prepare x axis
days=(etime0-stime0).days

## get projection info
GRIDFILE=root_dir+"/mcip/GRIDDESC_{ID}_{DOM}".format(ID=APPL,DOM=DOM)
with open(GRIDFILE) as f: file=f.readlines()
COORD=file[2].split(); GRID=file[5].split()

COORDTYPE=int(COORD[0])
P_ALP,P_BET,P_GAM,XCENT,YCENT=map(float,COORD[1:])
#XCENT=103.70
#YCENT=1.53

COORD_NAME=GRID[0]
XORIG,YORIG,DX,DY=map(float,GRID[1:5])
NCOLS,NROWS,NTHIK=map(int,GRID[5:])

lcc_x=[DX*NCOLS/2.0+XORIG+DX*j for j in range(NCOLS)]
lcc_y=[DY*NROWS/2.0+YORIG+DY*i for i in range(NROWS)]
mesh_lcc_x,mesh_lcc_y=np.meshgrid(lcc_x,lcc_y)

plt.ion()
plt.clf()
print("make Basemap object")
m = Basemap(resolution="i", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

## figure config
latlon_fs=14

m.drawcoastlines(linewidth=0.3)
m.drawcountries(color=("0.4"),linewidth=0.3)
#m.fillcontinents(color=(0.8,1,0.8))
m.fillcontinents(color="0.8")
m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], size=latlon_fs,dashes=[1,1],linewidth=0.5)
m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], size=latlon_fs,dashes=[1,1],linewidth=0.5)

## open position file
#fr="/usr601/senoo/run/EA.1201-1303/observation/metropolis.csv"
#POS_FILE=root_dir+"/tab/met_pos.csv"
POS_FILE=root_dir+"/tab/pm_pos.csv"
pos_array=np.genfromtxt(POS_FILE,delimiter=",",names=True,dtype=None)

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

## convert 1-D list of position  to 2-D mesh
base_lon,base_lat=m(pos_lon,pos_lat)

## plot observation
for i,city in enumerate(range(len(pos_array))):
    plt.plot(base_lon[i],base_lat[i],c=plt.cm.rainbow(i*290/len(pos_array)),marker=markers[i],label=pos_city[i],alpha=1,ms=8)

plt.legend(loc="lower left")
obstitle="Position of Observation"
#plt.title(obstitle,size=18)

if not os.path.exists(model_save_dir): os.makedirs(model_save_dir) 
plt.savefig(model_save_dir+"/met_pos.png",bbox_inches="tight")

## convert projected x, y to model col, row.
model_col=np.vectorize(round)(base_lon/DX -1.0).astype(int)
model_row=np.vectorize(round)(base_lat/DY -1.0).astype(int)

## extract data from model file
for day in range(days):
    stime=stime0+datetime.timedelta(days=day)
    print("open",stime,model_type)
#    fr=mydata+"/CCTM_parallel_cb05tucl_ae5_aq_CONC.EA.1201-1303_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day) 
    #MODEL_FILE=mydata+"/CCTM_parallel_saprc99_ae5_aq_CONC.{APPL}_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day,APPL=APPL) 
    MODEL_FILE=mydata+"/METCRO2D_{APPL}_{y}{m:02}{d:02}_D1".format(y=stime.year,m=stime.month,d=stime.day,APPL=APPL) 
    #model_nc=netcdf.netcdf_file(MODEL_FILE,"r")
    model_nc=netCDF4.Dataset(MODEL_FILE)

    if day == 0: ## extract variable list and variable unit
        varlist=model_nc.getncattr("VAR-LIST").split()
        varlist.sort()
        UNITLIST=[model_nc.variables[var].units.strip() for var in varlist]
#        varlist.extend("PM0.1 PM2.5 PM10".split())
#        UNITLIST=[word.replace("micrograms","ug") for word in UNITLIST]
#        UNITLIST=[word.replace("**","") for word in UNITLIST]
#        UNITLIST=UNITLIST+["ug/m3"]*3



    for ipos,position in enumerate(pos_city):
        if day ==0: ## write header
            FW=open(model_save_dir+"/"+position+".csv","w")
            FW.write("# description,"+"This data is extracted surface {model} output.".format(model=model_type.upper())+"\n")
            FW.write("# position,"+position+"\n")
            FW.write("# lon,"+str(pos_lon[ipos])+"\n")
            FW.write("# lat,"+str(pos_lat[ipos])+"\n")
            FW.write("# col,"+str(model_col[ipos])+"\n")
            FW.write("# row,"+str(model_row[ipos])+"\n")
            FW.write("# unit,"+",".join(UNITLIST)+"\n")
            FW.write("Date,"+",".join(varlist)+"\n")
            FW.close()
        for hour in range(24):
            FW=open(model_save_dir+"/"+position+".csv","aw")
            line=[stime.strftime("%Y%m%d")+"T"+str(hour).zfill(2)+"00Z"]
            for var in varlist:
                line.append(model_nc.variables[var][hour,0,model_row[ipos],model_col[ipos]])
            FW.write(",".join(map(str,line))+"\n")
            FW.close()
FW.close()
