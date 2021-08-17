#!/bin/bash
#
#
#
# NOTE:  you might need root access to install cmor python egg /usr/local/lib (See last line)
#
# -------------------
# Obtain all packages 
# -------------------

export CMOR_ROOT=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export BUILD_DIR=${CMOR_ROOT}/build
echo $BUILD_DIR
export GIT_SSL_NO_VERIFY=true 
export PREFIX=$HOME/$BUILD_DIR
# -------------------

ZLIB_URL=http://zlib.net
ZLIB_FILE=zlib-1.2.11.tar.gz
ZLIB_DIR=`echo $ZLIB_FILE | sed 's/\.tar.gz/\//g'`

HDF5_URL=https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.17/src
HDF5_FILE=hdf5-1.8.17.tar.gz
HDF5_DIR=`echo $HDF5_FILE | sed 's/\.tar.gz/\//g'`

NETCDF_URL=ftp://ftp.unidata.ucar.edu/pub/netcdf
NETCDF_FILE=netcdf-4.4.0.tar.gz
NETCDF_DIR=`echo $NETCDF_FILE | sed 's/\.tar.gz/\//g'`

EXPAT_URL=https://sourceforge.net/projects/expat/files/expat/2.1.0
EXPAT_FILE=expat-2.1.0.tar.gz
EXPAT_DIR=`echo $EXPAT_FILE | sed 's/\.tar.gz/\//g'`

#wget 
UDUNITS_URL=ftp://ftp.unidata.ucar.edu/pub/udunits
UDUNITS_FILE=udunits-2.2.23.tar.gz
UDUNITS_DIR=`echo $UDUNITS_FILE | sed 's/\.tar.gz/\//g'`

UUID_URL=http://www.mirrorservice.org/sites/ftp.ossp.org/pkg/lib/uuid
UUID_FILE=uuid-1.6.2.tar.gz
UUID_DIR=`echo $UUID_FILE | sed 's/\.tar.gz/\//g'`

# -------------------
if [ ! -d ${BUILD_DIR} ];then
    mkdir ${BUILD_DIR}
fi

cd ${BUILD_DIR}

if [ ! -f $ZLIB_FILE ]; then
    wget ${ZLIB_URL}/${ZLIB_FILE}
fi

if [ ! -f $HDF5_FILE ]; then
    wget ${HDF5_URL}/${HDF5_FILE}
fi

if [ ! -f $NETCDF_FILE ]; then
    wget ${NETCDF_URL}/${NETCDF_FILE}
fi

if [ ! -f $EXPAT_FILE ]; then
    wget ${EXPAT_URL}/${EXPAT_FILE}
fi

if [ ! -f $UDUNITS_FILE ]; then
    wget ${UDUNITS_URL}/${UDUNITS_FILE}
fi

if [ ! -f $UUID_FILE ]; then
    wget ${UUID_URL}/${UUID_FILE}
fi


#
# -------------------
# Untar packages
# -------------------
if [ ! -d $ZLIB_DIR ]; then
    tar xvzf ${ZLIB_DIR}
fi

if [ ! -d $HDF5_DIR ]; then
    tar xvzf ${HDF5_FILE}
fi

if [ ! -d $NETCDF_DIR ]; then
    tar xvzf ${NETCDF_FILE}
fi

if [ ! -d $EXPAT_DIR ]; then
    tar xvzf ${EXPAT_FILE}
fi

if [ ! -d $UDUNITS_DIR ]; then
    tar xvzf ${UDUNITS_FILE}
fi

if [ ! -d $UUID_DIR ]; then
    tar xvzf ${UUID_FILE}
fi

#
# -------------------
# BUILD ZLIB
# -------------------
#
 cd ${BUILD_DIR}/$ZLIB_DIR
./configure --prefix=$PREFIX
make 
make check
make install

#
# -------------------
# BUILD libuuid
# -------------------
#
cd ${BUILD_DIR}/$UUID_DIR
./configure --prefix=$PREFIX
make 
make check
make install


# -------------------
# build expat
# -------------------
cd ${BUILD_DIR}/${EXPAT_DIR}
./configure --prefix=$PREFIX
make
make install


#
# -------------------
# build udnits2
# -------------------
#
cd ${BUILD_DIR}/${UDUNITS_DIR}
./configure --prefix=$PREFIX
make
make install
exit 1

#
# -------------------
# build hdf5
# -------------------
#
cd ../$HDF5_DIR
./configure --prefix=$PREFIX
make  
make install
#
# -------------------
# build netcdf4
# -------------------
#
export CFLAGS="-I$HOME/build/include"
export LDFLAGS="-L$HOME/build/lib"

cd ../$NETCDF_DIR
./configure --prefix=$PREFIX --enable-netcdf4
make 
make install


#
# -------------------
# build cmor
# -------------------
cd ..
git clone https://github.com/PCMDI/cmor.git
cd cmor
git checkout cmor3

./configure --prefix=$PREFIX --with-python=$PREFIX --with-uuid=$PREFIX --with-udunits=$PREFIX --with-netcdf=$PREFIX
make 

#
#  For installing egg without su, temporarily set PYTHONPATH to a directory where you want to 
#  install it, such as e.g. "$HOME/.local/lib/python2.7/site-packages"
#
sudo make install
sudo make python
 
