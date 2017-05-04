#!/bin/bash
# \file install-nkf-latest.sh
# \author SENOO, Ken
# \copyright CC0

VER=2.1.3
cd ${LOCAL}/src
wget -nc http://dl.sourceforge.jp/nkf/59912/nkf-${VER}.tar.gz
VER=2.1.3 ./install-nkf-body.sh
