#!/bin/bash
# \file install-glibc-2.22.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <>

PKG=glibc
VER=2.22
SRC_URL="http://ftp.gnu.org/pub/gnu/${PKG}/${PKG}-${VER}.tar.xz"
DEPENDS=""
CONFIG_ARG=""

cd ../
source install-body.sh
