#!/bin/bash
# \file install-ncurses-latest.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <http://www.gnu.org/software/ncurses/ncurses.html>

DEPENDS=
PKG=ncurses
VER=6.0
SRC_URL="http://ftp.gnu.org/pub/gnu/${PKG}/${PKG}-${VER}.tar.gz"
[ $MSYSTEM != "" ] && CONFIG_ARG="CC=cc CXX=/usr/bin/g++"

cd ../
source install-body.sh
