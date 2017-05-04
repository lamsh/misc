#!/bin/bash
# \file install-template.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <>

PKG=stow
VER=2.2.0
SRC_URL="http://ftp.gnu.org/pub/gnu/${PKG}/${PKG}-${VER}.tar.gz"
DEPENDS=""
CONFIG_ARG=""

cd ../
source install-body.sh
