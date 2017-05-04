#!/bin/bash
# \file install-termcap.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <>

PKG=termcap
VER=1.3.1
SRC_URL="http://ftp.gnu.org/pub/gnu/${PKG}/${PKG}-${VER}.tar.gz"
DEPENDS=
CONFIG_ARG=

cd ../
source install-body.sh
