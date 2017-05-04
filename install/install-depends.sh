#!/bin/bash
# \file install-depends.sh
# \author SENOO, Ken
# \copyright CC0


DEPENDS="make"

[ "$(command -v pacman)" ] && MANAGER="pacman -S --noconfirm"
[ "$(command -v apt-get)" ] && MANAGER="apg-get -y install"

$MANAGER $DEPENDS
