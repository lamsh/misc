#!/bin/bash
# @author: SENOO, Ken
# (Last Update: 2014-05-22T00:17+09:00)

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)

wrf_dir=~/model/WRF/WRF-3.6/

ln -sf ${script_dir}/Daily-WRF.py ${wrf_dir}/
ln -sf ${script_dir}/namelist.wps.tmpl ${wrf_dir}/WPS/
ln -sf ${script_dir}/namelist.input.tmpl ${wrf_dir}/WRFV3/run/

