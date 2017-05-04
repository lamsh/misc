#!/bin/bash
# \file install-nkf-body.sh
# \author SENOO, Ken
# \copyright CC0

tar zxf nkf-${VER}.tar.gz
cd nkf-${VER}
make && make install prefix=${LOCAL}/stow/nkf-${VER} MKDIR="mkdir -p"
cd ${LOCAL}/stow
stow nkf-${VER}
