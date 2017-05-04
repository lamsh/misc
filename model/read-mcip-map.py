#!/bin/env python2.7
# coding: utf-8
# @author: SENOO Ken

## load MCIP output file and plot mapping hourly and day average  

## policy
## plot variables by loop

from scipy.io import netcdf
import datetime
import dateutils
import calendar
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib

import numpy as np
import os
import sys


## set save directory
model_type="mcip"
#run_name="EA.1201-1303"
run_name="CJ.201301-201303"
DOM="D1"
root_dir="/usr601/senoo/run/{run_id}".format(run_id=run_name)
save_dir="fig/{0}".format(model_type)
#mech="saprc-99"
mech=""
whether_megan=""
mid_dir=mech+"/"+whether_megan+"/map"
title_desc="" # with MEGAN
title_mech=mech.upper() # SAPRC-99
mask_value=10e-6

## input file directory
#input_dir="/usr601/senoo/run/EA.1201-1303/smoke/saprc-99/with_megan"
input_dir="{dir}/{type}".format(type=model_type,mech=mech,whether_megan=whether_megan,dir=root_dir)

## 
stat=["max", "mean", "min"]
timespan=["hourly", "daily", "weekly", "monthly","yearly"]

for i in timespan:
        if not os.path.exists(save_dir+"/"+mid_dir+"/"+i): os.makedirs(save_dir+"/"+mid_dir+"/"+i)

## set date
(styear,stmonth,stday,sthour) = (2013,1,1,0)
(enyear,enmonth,enday,enhour) = (2013,4,2,0)

stime0=datetime.datetime(styear,stmonth,stday,sthour)
etime0=datetime.datetime(enyear,enmonth,enday,sthour)

## prepare x axis
days=(etime0-stime0).days
xday=[stime0+datetime.timedelta(days=i) for i in xrange(days)]
hours=24*days
xhour=[stime0+datetime.timedelta(hours=i) for i in xrange(hours)]
weeks=days/7
xweek=[stime0+datetime.timedelta(weeks=i) for i in xrange(weeks)]
months=(etime0.year-stime0.year)*12+(etime0.month-stime0.month)
xmonth=[stime0+dateutils.relativedelta(months=i) for i in xrange(months)]

## date formatting
ymd="{y:04}{m:02}{d:02}".format(y=styear, m=stmonth, d=stday)

## 
cmap=cm.jet
cmap.set_under("w",alpha=0)
cmap.set_bad(color="white")

## get projection info
gridfile=root_dir+"/mcip/GRIDDESC_EA.1201-1303_D1"
gridfile=root_dir+"/mcip/GRIDDESC_"+run_name+"_"+DOM
with open(gridfile) as f: file=f.readlines()
COORD=file[2].split(); GRID=file[5].split()

COORDTYPE=int(COORD[0])
P_ALP,P_BET,P_GAM,XCENT,YCENT=map(float,COORD[1:])

COORD_NAME=GRID[0]
XORIG,YORIG,DX,DY=map(float,GRID[1:5])
NCOLS,NROWS,NTHIK=map(int,GRID[5:])

lcc_x=[DX*NCOLS/2.0+XORIG+DX*j for j in range(NCOLS)]
lcc_y=[DY*NROWS/2.0+YORIG+DY*i for i in range(NROWS)]
mesh_lcc_x,mesh_lcc_y=np.meshgrid(lcc_x,lcc_y)

plt.clf()
print("make Basemap object")
m = Basemap(resolution="i", projection="lcc", lat_1=P_ALP, lat_2=P_BET, width=DX*(NCOLS-1), height=DY*(NROWS-1), lat_0=YCENT, lon_0=XCENT, rsphere=(6370000.0, 6370000.0))


## figure config
latlon_fs=14

for day in range(days):
    stime=stime0+datetime.timedelta(days=day)
    print("open",stime)
    with open(input_dir+"/METCRO2D_{run_id}_{y}{m:02}{d:02}_D1".format(y=stime.year,m=stime.month,d=stime.day,run_id=run_name)) as f:
        mcip_nc=netcdf.netcdf_file(f,"r")

    ## ._attributes["VAR-LIST"]
## make variable list and smoke variable array for daily min, max, mean in domain.  
    if day == 0: 
        varlist_mcip=mcip_nc._attributes["VAR-LIST"].split()
#        with open(save_dir+"/"+mech+"/"+whether_megan+"/var_list_{model}.dat".format(mech=mech,whether_megan=whether_megan,model=model_type),"w") as f: np.array(varlist_mcip).tofile(f, sep=" ")         
        varlist_mcip="PRSFC TEMP2 TEMPG PBL WSPD10 WDIR10".split()

## initialize mcip_array
#        for time in timespan:
        mcip_array={time:{var:{stat:np.zeros(shape=(NROWS,NCOLS)) for stat in stat} for var in varlist_mcip} for time in timespan}
        [mcip_array[time][var].update({"unit": mcip_nc.variables[var].units.strip()}) for time in timespan for var in varlist_mcip]
        [mcip_array[time][var].update({"hour": range(24)}) for time in timespan for var in varlist_mcip]

## mask value zero to NaN for plot
    for var in varlist_mcip:
        for hour in range(24):
            test_nc=mcip_nc.variables[var][hour,0]; test_nc[test_nc<=mask_value]=np.nan
            mcip_array["hourly"][var]["hour"][hour]=np.ma.array(test_nc,mask=np.isnan(test_nc))
##
#    print("plotting hourly value")
    for var in varlist_mcip:
        for hour in range(24):
            break
            print("plot hourly value",stime,hour)
            plt.clf()
            now="{year:04}-{month:02}-{day:02}T{hour:02}:00Z".format(year=stime.year, month=stime.month, day=stime.day, hour=hour)
            m.drawcoastlines(); m.drawcountries()
            m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=latlon_fs)
            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
        ## for human readable plot
        #  plt.contourf(lcc_x, lcc_y, mcip_nc.variables[var][hour,0],extend="both",cmap=cmap)
        ## plot for grid readable plot
            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,mcip_array["hourly"][var]["hour"][hour] ,cmap=cmap)
            plt.colorbar(pad=0.01,fraction=0.1,extend="both").ax.tick_params(labelsize=14)
            plt.title("Hourly MCIP output {var_name} {desc}\non surface at {time}".format(var_name=var,desc=title_desc, time=now),size=18,y=1.0)
            plt.figtext(0.8,0.91,"[{unit}]".format(unit=mcip_nc.variables[var].units.strip()),size=14)
            plt.savefig("{dir}/{mid}/hourly/{model}_hourly_{var}_{year:04}{month:02}{day:02}T{hour:02}00.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,whether_megan=whether_megan,model=model_type),bbox_inches="tight",dpi=60)


## Can you minimize below code by for loop?
## daily
#    for var in varlist_mcip: mcip_array["daily"][var]["mean"]=np.mean(np.dstack(mcip_nc.variables[var][:24,0]),axis=2,dtype=np.float128)
    for var in varlist_mcip: mcip_array["daily"][var]["mean"]=np.mean(np.ma.dstack(mcip_array["hourly"][var]["hour"][:]),axis=2,dtype=np.float128)

    print("plotting daily value")
    for var in varlist_mcip:
#        break
        plt.clf()
        now="{year:04}-{month:02}-{day:02}".format(year=stime.year, month=stime.month, day=stime.day, hour=hour)
        m.drawcoastlines();  m.drawcountries()
        m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=latlon_fs)
        m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
#        plt.contourf(lcc_x, lcc_y, mcip_array["daily"][var]["mean"],cmap=cmap)
        plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,mcip_array["daily"][var]["mean"] ,cmap=cmap)
        plt.colorbar(pad=0.01,fraction=0.1,extend="both").ax.tick_params(labelsize=14)
        plt.title("Daily MCIP output {var_name} {desc}\non surface at {time}".format(var_name=var,desc=title_desc, time=now),size=18,y=1.0)
        plt.figtext(0.8,0.91,"[{unit}]".format(unit=mcip_nc.variables[var].units.strip()),size=14)
        plt.savefig("{dir}/{mid}/daily/{model}_daily_{var}_{year:04}{month:02}{day:02}.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,whether_megan=whether_megan,model=model_type),bbox_inches="tight",dpi=60)


    ## weekly
    for var in varlist_mcip: mcip_array["weekly"][var]["mean"]+=mcip_array["daily"][var]["mean"]
    if (day+1) % 7 == 0:
        print("plotting weekly value")
        ago_week=(stime-datetime.timedelta(days=6))
        title_week="{y1}-{m1:02}-{d1:02} to {y2}-{m2:02}-{d2:02}".format(y1=ago_week.year,m1=ago_week.month,d1=ago_week.day,y2=stime.year,m2=stime.month,d2=stime.day)
        for var in varlist_mcip:
            break
            mcip_array["weekly"][var]["mean"]=np.ma.array(mcip_array["weekly"][var]["mean"],mask=np.isnan(mcip_array["weekly"][var]["mean"]))
            plt.clf()
            mcip_array["weekly"][var]["mean"]/=7.0
            m.drawcoastlines(); m.drawcountries()
            m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=latlon_fs)
            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
        #    plt.contourf(lcc_x, lcc_y, mcip_array["weekly"][var]["mean"]cmap=cmap)
            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,mcip_array["weekly"][var]["mean"] ,cmap=cmap)
            plt.colorbar(pad=0.01,fraction=0.1,extend="both",).ax.tick_params(labelsize=14)
            plt.title("Weekly MCIP output {var_name} {desc}\non surface at {time}".format(var_name=var,desc=title_desc, time=title_week ),size=18,y=1.0)
            plt.figtext(0.8,0.91,"[{unit}]".format(unit=mcip_nc.variables[var].units.strip()),size=14)
            plt.savefig("{dir}/{mid}/weekly/{model}_weekly_{var}_{year:04}{month:02}{day:02}.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,whether_megan=whether_megan,model=model_type),bbox_inches="tight",dpi=60)
        mcip_array["weekly"][var]["mean"]=0.0
    
    
    ## monthly
    for var in varlist_mcip: mcip_array["monthly"][var]["mean"]+=mcip_array["daily"][var]["mean"]
    if stime.day == calendar.monthrange(stime.year,stime.month)[1]: 
        print("plotting monthly value")

        for var in varlist_mcip:
#            break
            a=mcip_array["monthly"][var]["mean"]; a[a<=1.0e-10]=np.nan
            mcip_array["monthly"][var]["mean"]=np.ma.array(mcip_array["monthly"][var]["mean"],mask=np.isnan(a))
            plt.clf()
            mcip_array["monthly"][var]["mean"]/=float(calendar.monthrange(stime.year,stime.month)[1])
            m.drawcoastlines(); m.drawcountries()
            m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=latlon_fs)
            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
#            plt.contourf(lcc_x, lcc_y, mcip_array["monthly"][var]["mean"],extend="both",cmap=cmap)
            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,mcip_array["monthly"][var]["mean"] ,cmap=cmap)
            plt.colorbar(pad=0.01,fraction=0.1,extend="both",).ax.tick_params(labelsize=14)
            plt.title("Monthly MCIP output {var_name} {desc}\non surface at {y}-{m:02}".format(var_name=var,desc=title_desc, y=stime.year,m=stime.month),size=18,y=1.0)
            plt.figtext(0.8,0.91,"[{unit}]".format(unit=mcip_nc.variables[var].units.strip()),size=14)
            plt.savefig("{dir}/{mid}/monthly/{model}_monthly_{var}_{year:04}{month:02}.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,whether_megan=whether_megan,model=model_type),bbox_inches="tight",dpi=60)
        mcip_array["monthly"][var]["mean"]=0.0


    ## yearly
    for var in varlist_mcip: mcip_array["yearly"][var]["mean"]+=mcip_array["daily"][var]["mean"]
    if (stime.month, stime.day) == ((stime0+dateutils.relativedelta(months=11)).month, calendar.monthrange(stime.year,stime.month)[1]): 
        print("plotting yearly value")
        for var in varlist_mcip:
            plt.clf()
            mcip_array["yearly"][var]["mean"]/=float(day+1)
            mcip_array["yearly"][var]["mean"]=np.ma.masked_less_equal(cctm_array["yearly"][var]["mean"],mask_value)
            m.drawcoastlines(); m.drawcountries()
            m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=latlon_fs)
            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
#            plt.contourf(lcc_x, lcc_y, mcip_array["yearly"][var]["mean"],extend="both",cmap=cmap)
            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,mcip_array["yearly"][var]["mean"] ,cmap=cmap)
            plt.colorbar(pad=0.01,fraction=0.1,extend="both",).ax.tick_params(labelsize=14)
            plt.title("Yearly {model} {var_name} {desc}\non surface at {syear}-{smonth:02} to {eyear}-{emonth:02}".format(var_name=var,desc=title_desc, time=stime.year,mech=mech.upper(),syear=stime0.year,smonth=stime0.month,eyear=stime.year,emonth=stime.month,model=model_type.upper()),size=18,y=1.0)
            plt.figtext(0.8,0.91,"[{unit}]".format(unit=mcip_nc.variables[var].units.strip()),size=14)
            plt.savefig("{dir}/{mid}/yearly/{model}_yearly_{var}_{mech}_{whether_megan}_{syear:04}{smonth:02}-{eyear}{emonth:02}.png".format(dir=save_dir,mid=mid_dir,var=var,syear=stime0.year,smonth=stime0.month,eyear=stime.year,emonth=stime.month,mech=mech,whether_megan=whether_megan,model=model_type),bbox_inches="tight",dpi=60)
            mcip_array["yearly"][var]["mean"]=0.0
