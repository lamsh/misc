#!/bin/bash
# \file install-bash-body.sh
# \author SENOO, Ken
# \copyright CC0
# \date 2015-09-29T20:34+09:00

./configure --prefix=${LOCAL}/stow/bash-${VER}
make && make install
cd ${LOCAL}/stow; stow bash-${VER}


