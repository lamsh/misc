#!/bin/bash
# @author: SENOO, Ken
# (Last Update: 2014-05-20T10:01+09:00)

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)

paste_dir=~/model/WRF/script/
mkdir -p ${paste_dir}

for i in  ${script_dir}/*.py
do
    ln -sf  $i  ${paste_dir}
done

