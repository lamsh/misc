#!/bin/bash
# \file install-template.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <>

PKG=diffutils
VER=3.3
SRC_URL="http://ftp.gnu.org/pub/gnu/${PKG}/${PKG}-${VER}.tar.xz"
DEPENDS=""
CONFIG_ARG=""

cd ../
source install-body.sh
