#!/bin/bash
# \file install-tar-latest.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <https://www.gnu.org/software/tar/>

PKG=tar
VER=1.28
SRC_URL="http://ftp.gnu.org/pub/gnu/${PKG}/${PKG}-${VER}.tar.gz"
DEPENDS=""
# CONFIG_ARG="--build=x86_64-w64-mingw32"

cd ../
source install-body.sh
