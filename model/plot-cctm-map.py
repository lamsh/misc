#!/bin/env python2.7
# coding: utf-8
# @author: SENOO Ken

## load CCTM output file and plot mapping hourly and day average  

from scipy.io import netcdf
import datetime
import dateutils
import calendar
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.dates as mdates

import numpy as np
import os
import sys


## set save directory
model_type="cctm"
APPL="CJ.201301-201303"
root_dir="/usr601/senoo/run/{run_id}".format(run_id=APPL)
save_dir="fig/{0}".format(model_type)
mech="saprc-99"#cb05
#mech="cb05"
#is_megan="without_megan"
is_megan="with_megan"
is_mozart="without_mozart"
fig_type="map"
#mid_dir="/"+"/".join([mech, is_megan, is_mozart, fig_type])
mid_dir="/"+fig_type+"/"
## title_desc=without MEGAN with MOZART
#title_desc=" ".join([i.split("_")[0]+" "+i.split("_")[1].upper() for i in [is_megan, is_mozart]])
title_desc="" # " ".join([i.split("_")[0]+" "+i.split("_")[1].upper() for i in [is_megan, is_mozart]])


## open file
#mydata="{dir}/{type}/{mech}/{is_megan}/without_mozart".format(type=model_type,mech=mech,is_megan=is_megan,dir=root_dir)
mydata="{dir}/{type}/{mech}/{is_megan}/{is_mozart}".format(type=model_type,mech=mech,is_megan=is_megan,dir=root_dir,is_mozart=is_mozart)

MIN_MASK=-0.1e-10
MAX_MASK=1.0e10
FS_TITLE=14

## 
stat=["max", "mean", "min"]
timespan=["hourly", "daily", "weekly", "monthly","yearly"]

for i in timespan:
    if not os.path.exists(save_dir+"/"+mid_dir+"/"+i):
        os.makedirs(save_dir+"/"+mid_dir+"/"+i)
# for i in timespan: os.makedirs(save_dir+"/"+mid_dir+"/"+i) if not os.path.exists(save_dir+"/"+mid_dir+"/"+i) else 0

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
cmap=plt.cm.jet
#cmap.set_under("w",alpha=0)
#cmap.set_bad(color="white")

## get projection info
gridfile=root_dir+"/mcip/GRIDDESC_{run_id}_D1".format(run_id=APPL)
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
latlon_fs=16

## PM2.5 equation from CCTM
# 
# ASO4I + ASO4J + ANH4I + ANO3I +ANO3J + AALKJ + AOLGAJ +ATOL1J + ATOL2J + ATOL3J + AXYL1J + AXYL2J + AXYL3J + AOLGBJ + ATRP1J +ATRP2J + AISO1J +AISO2J + AISO3J + 1.167* AORGPAI+ 1.167*AORGPAJ+ AECI +AECJ +A25I +A25J

varlist_pm25="""ASO4I  ASO4J  ANH4I ANH4J ANO3I ANO3J  AALKJ  AOLGAJ ATOL1J  ATOL2J  ATOL3J  AXYL1J  AXYL2J  AXYL3J  AOLGBJ  ATRP1J ATRP2J  AISO1J AISO2J  AISO3J   AORGPAI AORGPAJ AECI AECJ A25I A25J""".split()

CRANGE={
    "CO": np.arange(0,1.1,0.1),
    "NO2": np.arange(0,0.055,0.005),
    "SO2": np.arange(0,0.055,0.005),
    "O3": np.arange(0,0.11, 0.01),
    "PM0.1": np.arange(0,22, 2),
    "PM2.5": np.arange(0,220, 20),
    "PM10": np.arange(0,220, 20)}
for day in range(days):
    stime=stime0+datetime.timedelta(days=day)
    print("open",stime, mech, is_megan, is_mozart)
#    f=mydata+"/CCTM_parallel_cb05tucl_ae5_aq_CONC.EA.1201-1303_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day)
#    f=mydata+"/CCTM_parallel_saprc99_ae5_aq_CONC.{APPL}_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day,APPL=APPL)
    f=root_dir+"/"+model_type+"/standard/"+"/CCTM_parallel_saprc99_ae5_aq_CONC.{APPL}_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day,APPL=APPL)
#    with open(mydata+"/CCTM_parallel_saprc99_ae5_aq_CONC.EA.1201-1303_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day)) as f:
#    with open(mydata+"/CCTM_parallel_cb05tucl_ae5_aq_CONC.EA.1201-1303_{y}{m:02}{d:02}_D1.nc".format(y=stime.year,m=stime.month,d=stime.day)) as f:
    cctm_nc=netcdf.netcdf_file(f,"r")

    ## ._attributes["VAR-LIST"]
## make variable list and cctm variable array for daily min, max, mean in domain.  
    if day == 0: 
        varlist_cctm=cctm_nc._attributes["VAR-LIST"].split()
        varlist_cctm.sort()

## if PM2.5 species is not found in model output, delete target species.
#        for var in varlist_pm25:
#            if not var in varlist_cctm:
#                print("PM2.5 species "+var+" is not found in model output.")
#                varlist_pm25.remove(var)

## modify varlist for speedup
        ## PM variable list. PM01 = sum of A<hoge>I+1.167*AORGPAI. PM2.5 = PM01+sum of A<hoge>J + 1.167*AORGPAJ. PM10 = PM2.5+sum of A<hoge>K +ACORS+ASOIL+ASEAS
        pm01varlist=[var for var in varlist_cctm if var[0]=="A" and var[-1]=="I" and "AH2O" not in var]
        pm25varlist=[var for var in varlist_cctm if var[0]=="A" and var[-1]=="J" and "AH2O" not in var]
        pm10varlist=[var for var in varlist_cctm if var[0]=="A" and var[-1]=="K" and "AH2O" not in var or var in "ACORS ASOIL ASEAS".split()]

#        varlist_cctm=[var for var in varlist_pm25]
##        varlist_cctm.extend(["CO","NO2","NO","SO2","ISOPRENE","ETHENE","ACET"])
#        varlist_cctm.extend(["CO","NO2","SO2","O3"])
#        varlist_cctm_pm=[var for var in varlist_pm25]
#        #varlist_cctm_pm.extend(["PM2.5","CO","NO2","SO2","O3"])
#        varlist_cctm_pm.extend(["PM2.5"]+varlist_cctm)


## initialize cctm_array
#        for time in timespan:
        cctm_array={time:{var:{stat:np.zeros(shape=(NROWS,NCOLS)) for stat in stat} for var in varlist_cctm} for time in timespan}
        [cctm_array[time][var].update({"unit": cctm_nc.variables[var].units.strip()}) for time in timespan for var in varlist_cctm]
#        [cctm_array[time][var].update({"hour": [np.zeros(shape=(NROWS,NCOLS)) for i in range(24)]}) for time in timespan for var in varlist_cctm]
        [cctm_array[span][var].update({"hour": range(24)}) for span in ["hourly"] for var in varlist_cctm]
        for time in timespan:
            for var in varlist_cctm: 
                if cctm_array[time][var]["unit"] == "micrograms/m**3": cctm_array[time][var]["unit"]="ug/m3" 

#### add PM2.5 variables
##        for span in timespan: cctm_array[span]["PM2.5"]={stat:np.zeros(shape=(NROWS,NCOLS)) for stat in stat}
###        [cctm_array[span][var].update({"hour": [np.zeros(shape=(NROWS,NCOLS)) for i in range(24)   ] }) for span in timespan for var in ["PM2.5"]]
##        [cctm_array[span][var].update({"unit": "ug/m3"}) for span in timespan for var in ["PM2.5"]]

## add PM2.5 variables
        PMVAR="PM0.1 PM2.5 PM10".split()
        varlist_cctm.extend(PMVAR)
        for pmvar in PMVAR:
            for span in timespan: cctm_array[span][pmvar]={stat:np.zeros(shape=(NROWS,NCOLS)) for stat in stat}
#        [cctm_array[span][var].update({"hour": [np.zeros(shape=(NROWS,NCOLS)) for i in range(24)   ] }) for span in timespan for var in ["PM2.5"]]
        [cctm_array[span][var].update({"unit": "ug/m3"}) for span in timespan for var in PMVAR]

## mask value zero and tiny valu for plot
#    for hour in range(24):
#        for var in varlist_cctm:
##            cctm_array["hourly"][var]["hour"][hour]=np.ma.masked_less_equal(cctm_nc.variables[var][hour,0],MIN_MASK)
#            cctm_array["hourly"][var]["hour"][hour]=np.ma.masked_outside(cctm_nc.variables[var][hour,0],MIN_MASK,MAX_MASK)
##            temp=np.array(cctm_nc.variables[var][hour,0])
##            temp[(temp<MIN_MASK) | (MAX_MASK<temp)]=np.nan
##            cctm_array["hourly"][var]["hour"][hour]=temp

#    for var in varlist_cctm:
#        cctm_array["hourly"][var]["hour"]=[np.ma.masked_less_equal(cctm_nc.variables[var][hour,0],MIN_MASK) for hour in range(24)]

## calculation PM
    for pmvar in PMVAR:
        cctm_array["hourly"][pmvar]["hour"]= [np.zeros(shape=(NROWS,NCOLS)) for i in range(24) ] 
    for var in varlist_cctm:
        for hour in range(24):
            if var=="PM0.1":
                for pm01var in pm01varlist:
                    if pm01var == "AORGPAI":
                        cctm_array["hourly"][var]["hour"][hour]+=1.167*(cctm_nc.variables[pm01var][hour,0])
                    else:
                        cctm_array["hourly"][var]["hour"][hour]+=(cctm_nc.variables[pm01var][hour,0])
            elif var=="PM2.5":
                cctm_array["hourly"][var]["hour"][hour]+=cctm_array["hourly"]["PM0.1"]["hour"][hour]
                for pm25var in pm25varlist:
                    if pm25var == "AORGPAJ":
                        cctm_array["hourly"][var]["hour"][hour]+=1.167*(cctm_nc.variables[pm25var][hour,0])
                    else:
                        cctm_array["hourly"][var]["hour"][hour]+=(cctm_nc.variables[pm25var][hour,0])
            elif var=="PM10":
                cctm_array["hourly"][var]["hour"][hour]+=cctm_array["hourly"]["PM2.5"]["hour"][hour]
                for pm10var in pm10varlist:
                    cctm_array["hourly"][var]["hour"][hour]+=(cctm_nc.variables[pm10var][hour,0])
            else:
                cctm_array["hourly"][var]["hour"][hour]=np.ma.masked_less_equal(cctm_nc.variables[var][hour,0],MIN_MASK)
                    


#    [cctm_array[span][var].update({"hour": [np.zeros(shape=(NROWS,NCOLS)) for i in range(24)   ] }) for span in ["hourly"] for var in ["PM2.5"]]
    # cctm_array["hourly"]["PM2.5"]["hour"]= [np.zeros(shape=(NROWS,NCOLS)) for i in range(24) ] 
#    for hour in range(24):
#        for var in varlist_pm25:
#            if var == "AORGPAI" or var == "AORGPAJ":
#                cctm_array["hourly"]["PM2.5"]["hour"][hour]+=1.167*(cctm_nc.variables[var][hour,0])
#            else:
#                cctm_array["hourly"]["PM2.5"]["hour"][hour]+=(cctm_array["hourly"][var]["hour"][hour]) 


#    print("plotting hourly value")
##    for hour in range(24):
##        for var in varlist_cctm_pm:
##            break
##            print("plot hourly value",stime,hour)
##            if var in varlist_pm25: continue
##            plt.clf()
##            now="{year:04}-{month:02}-{day:02}T{hour:02}:00Z".format(year=stime.year, month=stime.month, day=stime.day, hour=hour)
##            m.drawcoastlines(); m.drawcountries()
##            m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], fontsize=latlon_fs)
##            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
##        ## for human readable plot
##        #  plt.contourf(lcc_x, lcc_y, cctm_nc.variables[var][hour,0],extend="both",cmap=cmap)
##        ## plot for grid readable plot
##            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,cctm_array["hourly"][var]["hour"][hour] ,cmap=cmap,vmin=0.0)
##            plt.colorbar(pad=0.01,fraction=0.1,extend="both").ax.tick_params(labelsize=14)
##            plt.title("Hourly CCTM {mech} {var_name} {desc}\non surface at {time}".format(var_name=var,desc=title_desc, time=now, mech=mech.upper()),size=FS_TITLE,y=1.0)
##            plt.figtext(0.8,0.91,"[{unit}]".format(unit=cctm_array["hourly"][var]["unit"]),size=14)
###            plt.figtext(0.8,0.91,"[{unit}]".format(unit=cctm_nc.variables[var].units.strip()),size=14)
##            plt.savefig("{dir}/{mid}/hourly/{model}_hourly_{var}_{mech}_{is_megan}_{year:04}{month:02}{day:02}T{hour:02}00.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,is_megan=is_megan,model=model_type.upper()),bbox_inches="tight",dpi=60)


## Can you minimize below code by for loop?
## daily
    for var in varlist_cctm:
        cctm_array["daily"][var]["mean"]=np.mean(np.ma.dstack(np.ma.masked_outside(cctm_array["hourly"][var]["hour"][:],MIN_MASK,MAX_MASK )),axis=2,dtype=np.float128)

    print("plotting daily value")
#    for var in varlist_cctm_pm:
    for var in varlist_cctm:
        break
#        if var in varlist_pm25: continue
        plt.clf()
        now="{year:04}-{month:02}-{day:02}".format(year=stime.year, month=stime.month, day=stime.day, hour=hour)
        m.drawcoastlines(linewidth=0.5,color="k");  m.drawcountries(color="k")
        m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], fontsize=latlon_fs)
        m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
#        plt.contourf(lcc_x, lcc_y, cctm_array["daily"][var]["mean"],cmap=cmap)
        plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,cctm_array["daily"][var]["mean"] ,cmap=cmap,vmin=0.0)
        if var in CRANGE.keys():
            plt.colorbar(pad=0.01,fraction=0.1,extend="both",ticks=CRANGE[var]).ax.tick_params(labelsize=14)
            plt.clim(min(CRANGE[var]),max(CRANGE[var]))
        else:
            plt.colorbar(pad=0.01,fraction=0.1,extend="both").ax.tick_params(labelsize=14)
        plt.title("Daily CCTM {mech} {var_name} {desc}on surface at {time}".format(var_name=var,desc=title_desc, time=now,mech=mech.upper()),size=FS_TITLE,y=1.0)
        plt.figtext(0.8,0.91,"[{unit}]".format(unit=cctm_array["daily"][var]["unit"]),size=14)
        plt.savefig("{dir}/{mid}/daily/{model}_daily_{var}_{mech}_{year:04}{month:02}{day:02}.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,is_megan=is_megan,model=model_type.upper(),is_mozart=is_mozart),bbox_inches="tight",dpi=60)


##    ## weekly
##    for var in varlist_cctm_pm: cctm_array["weekly"][var]["mean"]+=cctm_array["daily"][var]["mean"]
##    if (day+1) % 7 == 0:
##        print("plotting weekly value")
##        ago_week=(stime-datetime.timedelta(days=6))
##        title_week="{y1}-{m1:02}-{d1:02} to {y2}-{m2:02}-{d2:02}".format(y1=ago_week.year,m1=ago_week.month,d1=ago_week.day,y2=stime.year,m2=stime.month,d2=stime.day)
##        for var in varlist_cctm_pm:
##            break
##            if var in varlist_pm25: continue
###            cctm_array["weekly"][var]["mean"]=np.ma.array(cctm_array["weekly"][var]["mean"],mask=np.isnan(cctm_array["weekly"][var]["mean"]))
##            cctm_array["weekly"][var]["mean"]/=7.0
###            cctm_array["weekly"][var]["mean"]=np.ma.masked_less_equal(cctm_array["weekly"][var]["mean"],MIN_MASK)
##            cctm_array["weekly"][var]["mean"]=np.ma.masked_outside(cctm_array["weekly"][var]["mean"],MIN_MASK,MAX_MASK)
##            plt.clf()
##            m.drawcoastlines(); m.drawcountries()
##            m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=latlon_fs)
##            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
##        #    plt.contourf(lcc_x, lcc_y, cctm_array["weekly"][var]["mean"]cmap=cmap)
##            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,cctm_array["weekly"][var]["mean"] ,cmap=cmap,vmin=0.0)
##            plt.colorbar(pad=0.01,fraction=0.1,extend="both",ticks=CRANGE[var]).ax.tick_params(labelsize=14)
##            plt.clim(min(CRANGE[var]),max(CRANGE[var]))
###            plt.colorbar(pad=0.01,fraction=0.1,extend="both",ticks=CRANGE[var]).ax.tick_params(labelsize=14)
##            plt.title("Weekly CCTM {mech} {var_name} {desc}\non surface at {time}".format(var_name=var,desc=title_desc, time=title_week,mech=mech.upper() ),size=FS_TITLE,y=1.0)
##            plt.figtext(0.8,0.91,"[{unit}]".format(unit=cctm_array["hourly"][var]["unit"]),size=14)
##            plt.savefig("{dir}/{mid}/weekly/{model}_weekly_{var}_{mech}_{is_megan}_{year:04}{month:02}{day:02}.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,is_megan=is_megan,model=model_type.upper()),bbox_inches="tight",dpi=60)
##        cctm_array["weekly"][var]["mean"]=0.0
    
    
    ## monthly
    for var in varlist_cctm: cctm_array["monthly"][var]["mean"]+=cctm_array["daily"][var]["mean"]
    if stime.day == calendar.monthrange(stime.year,stime.month)[1]: 
        print("plotting monthly value")
        for var in varlist_cctm:
#            break
#            if var in varlist_pm25: continue
            plt.clf()
            cctm_array["monthly"][var]["mean"]/=float(calendar.monthrange(stime.year,stime.month)[1])
            cctm_array["monthly"][var]["mean"]=np.ma.masked_less_equal(cctm_array["monthly"][var]["mean"],MIN_MASK)
            m.drawcoastlines(); m.drawcountries()
            m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], fontsize=latlon_fs)
            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
#            plt.contourf(lcc_x, lcc_y, cctm_array["monthly"][var]["mean"],extend="both",cmap=cmap)
            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,cctm_array["monthly"][var]["mean"] ,cmap=cmap,vmin=0.0,vmax=100)
#            plt.colorbar(pad=0.01,fraction=0.1,extend="both",ticks=CRANGE[var]).ax.tick_params(labelsize=14)
            if var in CRANGE.keys():
                plt.colorbar(pad=0.01,fraction=0.1,extend="both",ticks=CRANGE[var]).ax.tick_params(labelsize=14)
                plt.clim(min(CRANGE[var]),max(CRANGE[var]))
            else:
                plt.colorbar(pad=0.01,fraction=0.1,extend="both").ax.tick_params(labelsize=14)
            plt.title("Monthly CCTM {mech} {var_name} {desc}on surface at {y}-{m:02}".format(var_name=var,desc=title_desc, y=stime.year,m=stime.month,mech=mech.upper()),size=FS_TITLE,y=1.0)
            plt.figtext(0.8,0.91,"[{unit}]".format(unit=cctm_array["hourly"][var]["unit"]),size=14)
            plt.savefig("{dir}/{mid}/monthly/{model}_monthly_{var}_{mech}_{year:04}{month:02}.png".format(dir=save_dir,mid=mid_dir,var=var,year=stime.year,month=stime.month,day=stime.day,hour=hour,mech=mech,is_megan=is_megan,model=model_type.upper()),bbox_inches="tight",dpi=60)
        cctm_array["monthly"][var]["mean"]=0.0


    ## yearly
    for var in varlist_cctm: cctm_array["yearly"][var]["mean"]+=cctm_array["daily"][var]["mean"]
    if (stime.month, stime.day) == ((stime0+dateutils.relativedelta(months=11)).month, calendar.monthrange(stime.year,stime.month)[1]): 
        print("plotting yearly value")
        for var in varlist_cctm:
            if var in varlist_pm25: continue
            plt.clf()
            cctm_array["yearly"][var]["mean"]/=float(day+1)
            cctm_array["yearly"][var]["mean"]=np.ma.masked_less_equal(cctm_array["yearly"][var]["mean"],MIN_MASK)
            m.drawcoastlines(linewidth=0.5); m.drawcountries()
            m.drawparallels(range(-90, 90, 10), labels = [1,0,0,0], fontsize=latlon_fs)
            m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=latlon_fs)
#            plt.contourf(lcc_x, lcc_y, cctm_array["yearly"][var]["mean"],extend="both",cmap=cmap)
            plt.pcolormesh(mesh_lcc_x, mesh_lcc_y,cctm_array["yearly"][var]["mean"] ,cmap=cmap,vmin=0.0)
            plt.colorbar(pad=0.01,fraction=0.1,extend="both",ticks=CRANGE[var]).ax.tick_params(labelsize=14)
            plt.title("Yearly {model} {mech} {var_name} {desc}\non surface at {syear}-{smonth:02} to {eyear}-{emonth:02}".format(var_name=var,desc=title_desc, time=stime.year,mech=mech.upper(),syear=stime0.year,smonth=stime0.month,eyear=stime.year,emonth=stime.month,model=model_type.upper()),size=FS_TITLE,y=1.0)
            plt.clim(min(CRANGE[var]),max(CRANGE[var]))
            plt.figtext(0.8,0.91,"[{unit}]".format(unit=cctm_array["hourly"][var]["unit"]),size=14)
            plt.savefig("{dir}/{mid}/yearly/{model}_yearly_{var}_{mech}_{is_megan}_{is_mozart}_{syear:04}{smonth:02}-{eyear}{emonth:02}.png".format(dir=save_dir,mid=mid_dir,var=var,syear=stime0.year,smonth=stime0.month,eyear=stime.year,emonth=stime.month,mech=mech,is_megan=is_megan,is_mozart=is_mozart,model=model_type),bbox_inches="tight",dpi=60)
            cctm_array["yearly"][var]["mean"]=0.0
