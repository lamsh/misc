#!/bin/bash
# \file install-zsh-5.1.1.sh
# \author SENOO, Ken
# \copyright CC0
# URL: <http://zsh.sourceforge.net/Arc/source.html>

DEPENDS=ncurses
VER=5.1.1
PKG=zsh
SRC_URL="http://sourceforge.net/projects/${PKG}/files/${PKG}/${VER}/${PKG}-${VER}.tar.xz"

[ $OS == "Windows_NT" ] && echo "Cygwin is not supported"; exit
cd ../
source install-body.sh
