#! /bin/bash

CMIPdir=$1
targetdir='/data/GCM/CMIP5'

allfiles=`find $CMIPdir -type f|grep nc`
e=$allfiles
a=($e)

for i in $(seq 0 $((${#a[*]} - 1))); do

src=${a[$i]}
echo $src
fn=`echo $src|sed 's#.*/##g'`
fldstr=`echo $fn|sed 's/_/ /g'|sed 's/\.nc//'`
flds=($fldstr)
newdir=$targetdir/${flds[3]}/${flds[1]}/${flds[0]}/${flds[2]}/${flds[4]}
echo mkdir -p $newdir
mkdir -p $newdir
target=$newdir/$fn
echo mv -f $src $target
mv -f $src $target

done