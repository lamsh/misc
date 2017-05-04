#!/bin/bash
# (File name: wrf-install.sh)
# Author: SENOO, Ken
# (Last update: 2014-11-30T04:25+09:00)
# License: MIT

# 参照: http://www.slideshare.net/iesli/20141129-senooken-introductionofwrf
# WRFv3.6.1をインストールするスクリプトです。Ubuntu 14.04 64bitで動作を確認済み。
# 事前にstowをインストールしておく。また，gfortran, make, tcshもインストールしておく。まだなら，たとえば以下のapt-getでインストールする。
# sudo apt-get install stow gfortran make csh
#
# WVER変数にインストールしたいWRFのバージョンを書いて以下のコマンドで実行する。
# ./wrf-install.sh
#
# インストールが完了するまでに約30 minほどかかる。
# 標準ではコンパイラにgfortran+gccを使い，NetCDF-4をオン，sm+dmの並列計算を有効にしてビルドする。
# 3.6.1と違うバージョンのWRFをインストールする場合，WRFとWPSのconfigureで選択するオプションの数字が異なるので変更する。
#
# ifortでビルドしたければ，以下のコンパイラ変数を設定する。
# export FC=ifort
# export F90=ifort
# export CC=icc
# export CXXC=icpc
#
# また，WRFとWPSのconfigureで選択するオプションの数字を変更する。
#
# インストールが完了し，WRFを実行する前には，必ず.wrfrcファイルを以下のコマンドで実行して設定を読み込む。
# source .wrfrc

WVER=3.6.1
WRFDIR=${HOME}/model/WRF/WRF-${WVER}

mkdir -p ${WRFDIR}/local/src
cd ${WRFDIR}

echo '
## (File name: .wrfrc)

## directory
WRFDIR=${PWD}
LOCAL=${PWD}/local

## local library
export PATH="${PWD}/local/bin:$PATH"
export LD_LIBRARY_PATH="${PWD}/local/lib:$LD_LIBRARY_PATH"
export CPATH="${PWD}/local/include:$CPATH"
export MANPATH="${PWD}/local/man:$MANPATH"

## JasPer
export JASPERLIB=${PWD}/local/lib
export JASPERINC=${PWD}/local/include

## WRF configure
export WRF_EM_CORE=1 # explicitly defines which model core to build
export WRF_NMM_CORE=0 # explicitly defines which model core NOT to build 
export WRF_DA_CORE=0 # explicitly defines no data assimilation
export NETCDF=${PWD}/local/
export OMP_NUM_THREADS=4 # if you have OpenMP on your system, this is how to specify the number of threads 
# export MP_STACK_SIZE=64000000 # OpenMP blows through the stack size, set it large. However, if the model still crashes, it may be a problem of overspecifying stack size. Set stack size sufficiently large, but not unlimited. On some systems, the equivalent parameter could be KMP_STACKSIZE, or OMP_STACKSIZE
export WRFIO_NCD_LARGE_FILE_SUPPORT=1 # for generating lager than 2 GB netcdf file
' > .wrfrc
source .wrfrc

# WRF library
## JasPer
VER=1.900.1
cd $LOCAL/src/
wget -nc http://www.ece.uvic.ca/~frodo/jasper/software/jasper-$VER.zip
unzip -o jasper-$VER.zip
cd jasper-$VER
./configure --prefix=$LOCAL/stow/jasper-$VER
make -j 4 &> make.log
make install
cd $LOCAL/stow
stow jasper-$VER

## zlib
VER=1.2.8
cd $LOCAL/src
wget -nc http://zlib.net/zlib-$VER.tar.xz
tar Jxf zlib-$VER.tar.xz
cd zlib-$VER
./configure --prefix=$LOCAL/stow/zlib-$VER
make -j 4 check &> makecheck.log
make install
cd $LOCAL/stow
stow zlib-$VER

## libpng
VER=1.6.14
cd $LOCAL/src
wget -nc http://download.sourceforge.net/libpng/libpng-$VER.tar.xz
tar Jxf libpng-$VER.tar.xz
cd libpng-$VER
LDFLAGS=-L$LOCAL/lib ./configure --prefix=$LOCAL/stow/libpng-$VER
make -j 4 check &> makecheck.log
make install
cd $LOCAL/stow
stow libpng-$VER

## HDF5
VER=1.8.14
cd $LOCAL/src
wget -nc http://www.hdfgroup.org/ftp/HDF5/current/src/hdf5-$VER.tar.bz2
tar jxf hdf5-$VER.tar.bz2
cd hdf5-$VER
./configure --prefix=$LOCAL/stow/hdf5-$VER --enable-fortran --enable-fortran2003 --enable-cxx --with-zlib=$LOCAL --enable-hl --enable-shared
make -j 4 &> make.log
make install
cd $LOCAL/stow
stow hdf5-$VER

## NetCDF
### C library
VER=4.3.2
cd $LOCAL/src
wget -nc ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-$VER.tar.gz
tar zxf netcdf-$VER.tar.gz
cd $LOCAL/src/netcdf-$VER
# ./configure --prefix=${HOME}/local/stow/netcdf-$VER --disable-netcdf-4 --disable-dap
LDFLAGS=-L$LOCAL/lib ./configure --prefix=$LOCAL/stow/netcdf-$VER --enable-netcdf-4 --enable-dap --enable-shared
make check -j 4 &> makecheck.log
make install
### Fortran library
FVER=4.4.1
cd $LOCAL/src/
wget -nc ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-fortran-$FVER.tar.gz
tar zxf netcdf-fortran-$FVER.tar.gz
cd $LOCAL/src/netcdf-fortran-$FVER
NETCDF=$LOCAL/stow/netcdf-$VER
LDFLAGS=-L$NETCDF/lib ./configure --prefix=$NETCDF --enable-shared
make check  -j 4 &> makecheck.log
make install
cd $LOCAL/stow/
stow netcdf-$VER

## MPICH
unset F90
VER=3.1.3
cd $LOCAL/src
wget -nc http://www.mpich.org/static/downloads/$VER/mpich-$VER.tar.gz
tar zxf mpich-$VER.tar.gz
cd mpich-$VER
./configure --prefix=$LOCAL/stow/mpich-$VER
make -j 4 &> make.log
make install
cd $LOCAL/stow
stow mpich-$VER


## WRF
VER=${WVER}
# WRFDIR=~/model/WRF/WRF-$VER

mkdir -p $WRFDIR
cd $WRFDIR
wget -nc http://www.mmm.ucar.edu/wrf/src/WRFV$VER.TAR.gz
wget -nc http://www.mmm.ucar.edu/wrf/src/WPSV$VER.TAR.gz
tar zxf WRFV$VER.TAR.gz
tar zxf WPSV$VER.TAR.gz

### WRF-ARW
cd $WRFDIR/WRFV3
export NETCDF4=1 # ON NetCDF4
./configure << EOF
35
1
EOF
J="-j 8" ./compile em_real &> compile.log

### WPS
cd $WRFDIR/WPS/
./configure << EOF
3
EOF
sed  -i.back -e '47c                        -L$(NETCDF)/lib -lnetcdff -lnetcdf -lgomp' \
  -e '64cDM_FC               = mpif90' \
  ./configure.wps
./compile &> compile.log
