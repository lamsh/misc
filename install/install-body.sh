#!/bin/bash
# \file install-body.sh
# \author SENOO, Ken
# \copyright CC0

LOCAL=${HOME}/local

if [ "$DEPENDS" != "" ]; then
  for DEP in ${DEPENDS}; do
    [ ! -e $DEP ] && (echo "Install ${DEP}"; cd ${DEP}; ./install-${DEP}-latest.sh || exit)
  done
fi

[ "$(command -v wget)" ] && GET="wget -nc --trust-server-names"
[ "$(command -v curl)" ] && GET="curl -JLO"

STOW="stow --ignore='dir|gschemas.compiled|icon-theme.cache'"
[ "$PKG" == "stow" ] && STOW="./stow-${VER}/bin/stow"

TAR_BALL=${SRC_URL##*/}
# EXT=${SRC_URL##*.}

[ "$(command -v tar)" ] && TAR="tar -xf"
[ "$(command -v bsdtar)" ] && TAR="bsdtar -xf"

case "$SRC_URL" in
  *.tar.gz)
    [ "$(command -v pax)" ] && UNZIP="pax -zrf"
    [ "$(command -v tar)" ] && UNZIP="${TAR}"
    ;;
  *.tar.bz2) UNZIP="${TAR}";;
  *.tar.xz) UNZIP="${TAR}";;
  *.zip) UNZIP="zip";;
esac

[ "${CONFIG_ARG}" == "" ] && [ "$MSYSTEM" != "" ] && CONFIG_ARG="--build=x86_64-pc-cygwin"
CONFIG_ARG+=" LDFLAGS=-L${LOCAL}/lib"

source ./run-with-color.sh

cd ${LOCAL}/src
[ -f ${TAR_BALL} ] || run ${GET} "${SRC_URL}"
run ${UNZIP} ${TAR_BALL}
cd ${PKG}-${VER}
if [[  $PKG =~ glibc ]]; then
  mkdir build; cd build
  run ../configure  --prefix=${LOCAL}/stow/${PKG}-${VER} ${CONFIG_ARG}
else
  run ./configure  --prefix=${LOCAL}/stow/${PKG}-${VER} ${CONFIG_ARG}
fi
run make && make install
cd ${LOCAL}/stow
${STOW} ${PKG}-${VER}
