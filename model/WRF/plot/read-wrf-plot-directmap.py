#!/bin/env python27
# coding: utf-8
# @author: SENOO Ken


from scipy.io import netcdf
import datetime
import pyproj
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.mlab import griddata
from mpl_toolkits.axes_grid import make_axes_locatable
import matplotlib.axes as maxes
import numpy as np
import matplotlib.cm as cm

"""
conversion of obsevation latlon to model column
1. pyproj:	latlon	->	lcc
2. lcc2modelxy:	lcc	->	model x, y
3. 		model x, y ->	int
4. interp:	int	->	interp
"""

def lcc2modelxy(x,y,imax,jmax,dx):
    ### FIND X,Y in model grid
    xc = x/dx + imax/2.0 -1.0
    yc = y/dx + jmax/2.0 -1.0
    xu = x/dx + (imax+1)/2.0 -1.0
    yv = y/dx + (jmax+1)/2.0 -1.0
#
    return (xc,xu,yc,yv)

## set date
(styear,stmonth,stday,sthour) = (2013,01,01,00)
(enyear,enmonth,enday,enhour) = (2013,03,1,00)

stime0=datetime.datetime(styear,stmonth,stday,sthour)
etime0=datetime.datetime(enyear,enmonth,enday,sthour)

days=(etime0-stime0).days


## array_tk: array of day averaged Temperature [K]
## save header
array_tk = [["Date"]]
vel = [["Order"], ["Station"], ["Date"],["Height [m]"],["Latitude"], ["Longitude"], ["Pressure [hPa]"], ["Temperature [K]"], ["Temperature [degree C]"],["u [m/s]"], ["v [m/s]"], ["w [m/s]"]]

#
VAR_WRF = {"date":[], "time": [], "ymdh": [],
        "height": [], "col": [], "row": [], #"lon": [], "lat": [], "lcc_x": [], "lcc_y": [],
    # surface variable
        #"t2_c":[], "t2_k":[], "u10":[], "v10": [],
        "t2_c":[], "u10":[], "v10": [],
        #"p_t": [], "t_k": [], "t_c": [], "u": [], "v": [], "w": []} 
        "p_t": [], "t_c": [], "u": [], "v": [], "w": []} 

date1="%04d-%02d-%02d" % (stime0.year,stime0.month,stime0.day)

cnetcdf = "/usr601/senoo/run/cj_1212-1302/wrf/pbl-1/wrfout_d01_%s_00_00_00" % date1
nc = netcdf.netcdf_file(cnetcdf, 'r')

## read model domain info (only once)
dx = nc._attributes["DX"]
dy = nc._attributes["DY"]
#imax = nc._attributes["WEST-EAST_GRID_DIMENSION"] -1
#jmax = nc._attributes["SOUTH-NORTH_GRID_DIMENSION"] -1
x_dim = nc.dimensions["west_east"]
y_dim = nc.dimensions["south_north"]

cen_lat = nc._attributes["CEN_LAT"]
cen_lon = nc._attributes["CEN_LON"]
truelat1 = nc._attributes["TRUELAT1"]
truelat2 = nc._attributes["TRUELAT2"]
lay_stag = nc.dimensions["bottom_top_stag"]

p1 = pyproj.Proj("+proj=lcc +lat_1=%f +lat_2=%f +lat_0=%f +lon_0=%f +x_0=0 +y_0=0" % (truelat1, truelat2, cen_lat, cen_lon )) 
p2 = pyproj.Proj("+proj=longlat +datum=WGS84")

width_meters = dx * (x_dim - 1)
height_meters = dy * (y_dim - 1)

### plot variable
plt.clf() # clear previous plot
F = plt.gcf()

# plot base map
m = Basemap(resolution="i", projection="lcc", lat_1=truelat1, lat_2=truelat2, width=width_meters, height=height_meters, lat_0=cen_lat, lon_0=cen_lon, rsphere=(6370000.0, 6370000.0))
#m.drawcoastlines(color="white")
#m.drawcountries(color="white")
m.drawcoastlines()
m.drawcountries()
m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=16)
m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=16)

# input model lon, lat
model_lon,model_lat = (nc.variables["XLONG"][0], nc.variables["XLAT"][0])
model_lcc_x, model_lcc_y = m(model_lon, model_lat)
 
t2_c_ref_levels = range(-30,35,5)
p_ref_levels = range(700,1080,10)

ax = plt.subplot(111)
## read data 
for DAY in range(days):

 stime=stime0 + datetime.timedelta(days=DAY)
 etime=stime + datetime.timedelta(days=1)
# ptime=stime - datetime.timedelta(days=1)

 year1=stime.year
 mon1=stime.month
 day1=stime.day
 hour1=stime.hour
 min1=stime.minute
 date1="%04d-%02d-%02d" % (year1,mon1,day1)

 print DAY,date1

## import netcdf file
 cnetcdf = "/usr601/senoo/run/cj_1212-1302/wrf/pbl-1/wrfout_d01_%s_00_00_00" % date1
 nc = netcdf.netcdf_file(cnetcdf, 'r')
 vector_10 = np.sqrt(pow(nc.variables["U10"][:],2)+pow(nc.variables["U10"][:],2))
 for hour in range(24):
     print "plotting time", hour
     curtimestring = "%04d-%02d-%02dT%02d:00Z" % (year1, mon1, day1, hour)
     filetime = curtimestring.replace("-","").replace(":","")

#     """ # T2 start
     print "plot T2"
     t2_c = [i -273.15 for i in nc.variables["T2"][hour]]
     plt.contourf(model_lcc_x, model_lcc_y, t2_c, t2_c_ref_levels, extend="both")
     #if DAY == 0 and hour == 0:
     if hour == 0:
         plt.colorbar(pad=0.01,fraction=0.1)
     plt.title("WRF-ARW temperature [degree C] at 2 m on {now}".format(now=curtimestring))
     plt.savefig("t2_{0}.png".format(filetime), bbox_inches="tight")
#     """ # T2 end
 plt.clf()
 m.drawcoastlines() 
 m.drawcountries()
 m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=16)
 m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=16)
 for hour in range(24):
     print "plotting time", hour
     curtimestring = "%04d-%02d-%02dT%02d:00Z" % (year1, mon1, day1, hour)
     filetime = curtimestring.replace("-","").replace(":","")

#     """ # P start
     print "plot P"
     p_t = [(p + pb)/100.0 for p, pb in zip(nc.variables["P"][hour,0], nc.variables["PB"][hour,0])]

     P = plt.contourf(model_lcc_x, model_lcc_y, p_t, p_ref_levels, extend="both")
     #if DAY == 0 and hour == 0:
     if hour == 0:
         plt.colorbar(pad=0.01,fraction=0.1)
     plt.title("WRF-ARW pressure [hPa] at surface on {now}".format(now=curtimestring))
     plt.savefig("p_{0}.png".format(filetime), bbox_inches="tight")
#     """ # P end

# m.drawcoastlines() 
 for hour in range(24):
     print "plotting time", hour
     curtimestring = "%04d-%02d-%02dT%02d:00Z" % (year1, mon1, day1, hour)
     filetime = curtimestring.replace("-","").replace(":","")
#     """ # vel start
     print "plot velocity"

     plt.clf()
     m.drawcoastlines() 
     m.drawcountries()
     m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=16)
     m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=16)
     plt.title("WRF-ARW velocity field [m/s] at 10 m on {now}".format(now=curtimestring))
     #vector = [ math.sqrt(nc.variables["U10"][:]**2+nc.variables["V10"][:]**2) ]
     #vector = [ math.sqrt(u10**2+v10**2) for u10,v10 in (nc.variables["U10"][:], nc.variables["V10"][:]) ]

     plt.quiver(model_lcc_x, model_lcc_y, nc.variables["U10"][hour], nc.variables["V10"][hour], vector_10, linewidth = 1, units="xy", angles="xy", edgecolor="None", headaxislength=5)
#     if hour == 0:
     plt.colorbar(pad=0.01,fraction=0.1, extend="both")
     plt.savefig("vel_{0}.png".format(filetime), bbox_inches="tight")
#     """ # vel end 

 for hour in range(24):
     print "plotting time", hour
     curtimestring = "%04d-%02d-%02dT%02d:00Z" % (year1, mon1, day1, hour)
     filetime = curtimestring.replace("-","").replace(":","")
     plt.clf()
     m.drawcoastlines() 
     m.drawcountries()
     m.drawparallels(range(-90, 90, 5), labels = [1,0,0,0], fontsize=16)
     m.drawmeridians(range(-180, 180, 10), labels = [0,0,0,1], fontsize=16)

#     """ # Mix start
     print "plot mix {0}".format(curtimestring)
     plt.title("WRF-ARW T2 [degree C], U10, V10 [m/s], surface P [hPa] on {now}".format(now=curtimestring),size="medium")
     t2_c = [i -273.15 for i in nc.variables["T2"][hour]]
     plt.contourf(model_lcc_x, model_lcc_y, t2_c, t2_c_ref_levels, extend="both")
     #if DAY == 0 and hour == 0:
#     if hour == 0:
     plt.colorbar(pad=0.01,fraction=0.2)
     p_t = [(p + pb)/100.0 for p, pb in zip(nc.variables["P"][hour,0], nc.variables["PB"][hour,0])]

     #P = plt.contour(model_lcc_x, model_lcc_y, p_t, extend="both")
     P = plt.contour(model_lcc_x, model_lcc_y, p_t)
     plt.clabel(P,fmt="%d")
#     if hour == 0:
#         plt.colorbar(pad=0.01,fraction=0.1)


#     plt.quiver(model_lcc_x, model_lcc_y, nc.variables["U10"][hour], nc.variables["V10"][hour],linewidth = 1, units="xy", angles="xy", edgecolor="None", headaxislength=5)
     plt.quiver(model_lcc_x, model_lcc_y, nc.variables["U10"][hour], nc.variables["V10"][hour], vector_10,linewidth = 1, units="xy", angles="xy", edgecolor="None", headaxislength=5,cmap=cm.binary_r)
     #plt.quiver(model_lcc_x, model_lcc_y, nc.variables["U10"][hour], nc.variables["V10"][hour], vector_10, linewidth = 1, units="xy", angles="xy", edgecolor="None", headaxislength=5)
#     if hour == 0:
     plt.colorbar(orientation="horizontal",pad=0.05,fraction=0.1, extend="both")
     plt.savefig("mix_t2_p_v_{0}.png".format(filetime), bbox_inches="tight")
#     """ # vel end 

