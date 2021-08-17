#!/bin/bash

if [ $# -ne 4 ]; then echo "usage $0: <mip-era> <experiment> <frequency> <variable>"; exit 1; fi

ROOT_DIR="/data/team/cmip6/pdsi/"
#MODELS=("CESM2" "MRI-ESM2-0")
MODELS=("MRI-ESM2-0")

VMIP=$1; EXP=$2; FREQ=$3; VAR=$4

source ./functions.sh ${ROOT_DIR}

for MODEL in ${MODELS[@]}; do

#download files
    
    nc_download ${VMIP} ${MODEL} ${EXP} ${FREQ} ${VAR}

#read in files

#    FILES="`ls ${ROOT_DIR}/${VMIP}/${MODEL}/${EXP}/${FREQ}/${VAR}/${VAR}_*.nc`"

#get monthly averages
    
#    mon_avg ${VMIP} ${MODEL} ${EXP} ${FREQ} ${VAR} ${FILES}

#plot avg fields
    
#    avg_plot ${VMIP} ${MODEL} ${EXP} ${FREQ} ${VAR} ${FILES}

done    

