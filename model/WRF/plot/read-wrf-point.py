#!/usr/bin/env python2.7
# coding: utf-8
# @author: SENOO, Ken
# (Last Update: 2014-05-28T23:14+09:00)

'''
== Description ==
This Python program export surface variables of WRF output to csv file on specific longitude and latitude position. And plot observation position on WRF domain.

output file is made in OUTDIR variable by following name:
<position name>.csv
position.pdf
position.png


== Input position file ===
You must prepare target position data file.

Sample file("observation-position.csv") is following format:
Location,Longitude,Latitude
Hinohara-mura,139.11,35.73
Isahaya,130.017,32.8425

In observation file, you must prepare for 3 columns.
1. Location name.
2. Longitude.
3. Latitude.

Location name is used identifying position(ex: output csv file name).
And at least, 2 points data is required. Line 1 is column header. Bellow  line 2 are each position data.

In column header, order and character cases is ignored. But each column header fields need specific sequence of character.
    Location name column field: "loc" or "cit" or "cap".
    Longitude: "lon".
    Latitude: "lat".

Ex: following position file is OK.
long,lat,city
139.11,35.73,Hinohara-mura
130.017,32.8425,Isahaya


== Variables for modifying ==
* ROOTDIR: input and output root directory.
* OUTDIR: output directory.
* POS_DIR: position data file directory.
* POS_FILE: position file name.
* START_DATE: start date.
* END_DATE: end date. This day is not included for reading data.
* INFILE: WRF output file name.


== Optional ==
In position.pdf, if you don't like margin of latitude and longitude grid, you can modify space of grid by following method place.
BM.drawparallels(np.arange(np.floor(BM.llcrnrlat), np.ceil(BM.urcrnrlat), 1),labels=[1,0,0,0])
BM.drawmeridians(np.arange(np.floor(BM.llcrnrlon), np.ceil(BM.urcrnrlon), 1),labels=[0,0,0,1])
'''

"""
== Program flow ==
1. Import module.
2. Open file.
3. Get projection.
4. Get point(observation) position and convert.
5. Extract point data.
"""

import netCDF4
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os, sys
import datetime

MODEL_TYPE="WRF"
## directory setting
ROOTDIR="~/run/my-run/" # need modify
ROOTDIR=os.path.expanduser(ROOTDIR)
INDIR=ROOTDIR+"output/" # need modify
POSDIR=ROOTDIR+"observation/" # need modify
POS_FILE="observation-position.csv" # need modify

OUTDIR=ROOTDIR+"point/" # need modify
if not os.path.exists(OUTDIR): os.makedirs(OUTDIR)

## date setting
START_DATE=datetime.datetime(2013,6,1) # need modify
END_DATE=datetime.datetime(2013,6,4) # need modify
DAYS=END_DATE-START_DATE


for day in range(DAYS.days):
    today=START_DATE+datetime.timedelta(day)
    print(today.isoformat())
    INFILE="wrfout_d01_{date}_00:00:00".format(date=today.strftime("%Y-%m-%d")) # need modify
    MODEL_NC=netCDF4.Dataset(INDIR+INFILE)
    
    if day == 0:
        ## get variable list and unit list
        #VARLIST=MODEL_NC.variables.keys()
        VARLIST="Q2 PSFC T2 TH2 U10 V10 RAINC RAINSH RAINNC SNOWNC".split()
        VARLIST.sort()
        UNITLIST=[MODEL_NC.variables[var].units.strip() for var in VARLIST]
        DESCLIST=[MODEL_NC.variables[var].description for var in VARLIST]
#        VARLIST.extend("PM0.1 PM2.5 PM10".split())
#        UNITLIST=[word.replace("micrograms","ug") for word in UNITLIST]
#        UNITLIST=UNITLIST+["ug/m3"]*3

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
        BM=Basemap(resolution="i", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))

        plt.ion()
        plt.clf()
        PARAMS={
                "font.size": 18,
                "legend.fontsize": "medium",
                "lines.MARKERSize": 10,
                }
        plt.rcParams.update(PARAMS)

        BM.drawcoastlines()
        BM.fillcontinents(color=(0.8,1,0.8))
        #BM.drawparallels(np.arange(-90,90,1),labels=[0,1,0,0])
        #BM.drawmeridians(np.arange(-180,180,1),labels=[0,0,0,1])
        BM.drawparallels(np.arange(np.floor(BM.llcrnrlat), np.ceil(BM.urcrnrlat), 1),labels=[1,0,0,0])
        BM.drawmeridians(np.arange(np.floor(BM.llcrnrlon), np.ceil(BM.urcrnrlon), 1),labels=[0,0,0,1])


        POS_ARRAY=np.genfromtxt(POSDIR+POS_FILE,delimiter=",",names=True,dtype=None)

        ## automatically get lattitude laongitude column header from character  "lat", "lon".
        ## automatically get position column header  from character "loc" or "cit" or "cap".
        LON_LABEL="".join(filter(lambda x: "lon" in x.lower(), POS_ARRAY.dtype.names))
        LAT_LABEL="".join(filter(lambda x: "lat" in x.lower(), POS_ARRAY.dtype.names))
        POS_LABEL="".join(filter(lambda x: "loc" in x.lower() or "cit" in x.lower() or  "cap" in x.lower(), POS_ARRAY.dtype.names))
        ## get array of longitude, latitude, position name.
        pos_lon=POS_ARRAY[LON_LABEL]
        pos_lat=POS_ARRAY[LAT_LABEL]
        pos_city=POS_ARRAY[POS_LABEL]

        MARKERS="o p d D < > ^ v p s d D * d x 6 7".split()

        ## convert 1-D list of position  to 2-D mesh
        base_lon,base_lat=BM(pos_lon,pos_lat)

        ## plot observation
        for i,city in enumerate(range(len(POS_ARRAY))):
            plt.plot(base_lon[i],base_lat[i],c=plt.cm.rainbow(i*290/len(POS_ARRAY)),marker=MARKERS[i],label=pos_city[i],alpha=1)

        plt.legend(loc="best")
        obstitle="Position of Observation"
        plt.title(obstitle)

        #plt.savefig(ROOTDIR+"fig/position.pdf",bbox_inches="tight")
        plt.savefig(OUTDIR+"position.png",bbox_inches="tight")
        plt.savefig(OUTDIR+"position.pdf",bbox_inches="tight")

        ## convert projected x, y to model col, row.
        model_col=np.vectorize(round)(base_lon/DX -1.0).astype(int)
        model_row=np.vectorize(round)(base_lat/DY -1.0).astype(int)


    ## export surface WRF variables on position.
    for ipos,position in enumerate(pos_city):
        if day ==0: ## write header
            FW=open(OUTDIR+position+".csv","w")
            FW.write("# comment,"+"This data is extracted from surface {model} output.".format(model=MODEL_TYPE.upper())+"\n")
            FW.write("# position,"+position+"\n")
            FW.write("# lon,"+str(pos_lon[ipos])+"\n")
            FW.write("# lat,"+str(pos_lat[ipos])+"\n")
            FW.write("# col,"+str(model_col[ipos])+"\n")
            FW.write("# row,"+str(model_row[ipos])+"\n")
            FW.write("# MAPFAC_MX,"+str(MODEL_NC.variables["MAPFAC_MX"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# MAPFAC_MY,"+str(MODEL_NC.variables["MAPFAC_MY"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# COSALPHA,"+str(MODEL_NC.variables["COSALPHA"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# SINALPHA,"+str(MODEL_NC.variables["SINALPHA"][0,model_row[ipos], model_col[ipos]])+"\n")
            FW.write("# description,"+",".join(DESCLIST)+"\n")
            FW.write("# unit,"+",".join(UNITLIST)+"\n")
            FW.write("Date,"+",".join(VARLIST)+"\n")
            FW.close()
        
        ## write data
        for hour in range(24):
            FW=open(OUTDIR+position+".csv","aw")
            line=[today.strftime("%Y%m%d")+"T"+str(hour).zfill(2)+"00Z"]
            for var in VARLIST:
                line.append(MODEL_NC.variables[var][hour,model_row[ipos],model_col[ipos]])
            FW.write(",".join(map(str,line))+"\n")
            FW.close()
