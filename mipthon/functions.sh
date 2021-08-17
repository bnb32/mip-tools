#!/bin/bash

if [ $# -ne 1 ]; then echo "usage $0: <root directory>"; exit 1; fi

ROOT_DIR=$1

mon_avg() {
    VMIP=$1; MODEL=$2; EXP=$3; FREQ=$4; VAR=$5; FILES=$6
    DATA_DIR="${ROOT_DIR}/${VMIP}/${MODEL}/${EXP}/${FREQ}/${VAR}"
    if [[ ${FILES} ]]; then
        for MONTH in {01..12}; do
            OUTFILE="${DATA_DIR}/${MODEL}_${VAR}_${MONTH}.nc"
            echo "creating average file: ${OUTFILE}"
            if [[ ! -f ${OUTFILE} ]]; then
                ncra -O -d time,$((${MONTH#0}-1)),,12 -v ${VAR} ${FILES} "${OUTFILE}"
            else
                echo "$OUTFILE already exists"
            fi    
        done
    else
        echo "problem downloading data"; exit 1
    fi    
}

full_avg() {
    VMIP=$1; MODEL=$2; EXP=$3; FREQ=$4; VAR=$5; FILES=$6
    DATA_DIR="${ROOT_DIR}/${VMIP}/${MODEL}/${EXP}/${FREQ}/${VAR}"
    OUTFILE="${DATA_DIR}/${MODEL}_${VAR}.nc"
    if [[ ${FILES} ]]; then
        echo "creating average file: ${OUTFILE}"
        if [[ ! -f ${OUTFILE} ]]; then
            ncra -O -d time,0, -v ${VAR} ${FILES} "${OUTFILE}"
        else
            echo "$OUTFILE already exists"
        fi    
    else
        echo "problem downloading data"; exit 1
    fi    
}

nc_download() {
    VMIP=$1; MODEL=$2; EXP=$3; FREQ=$4; VAR=$5
    DATA_DIR="${ROOT_DIR}/${VMIP}/${MODEL}/${EXP}/${FREQ}/${VAR}"
    python ../retriever.py $VMIP -t $FREQ -ex $EXP -var $VAR -m $MODEL -d ${DATA_DIR}

}

avg_plot() {
    VMIP=$1; MODEL=$2; EXP=$3; FREQ=$4; VAR=$5
    DATA_DIR="${ROOT_DIR}/${VMIP}/${MODEL}/${EXP}/${FREQ}/${VAR}"
    OUTFILE="${DATA_DIR}/${MODEL}_${VAR}_monthly.png"
    echo "plotting average files: ${MODEL} ${VAR}"
    if [[ ! -f ${OUTFILE} ]]; then
        python ./plot_multi_avg_map.py ${MODEL} ${VAR} ${DATA_DIR}
    else
        echo "${OUTFILE} already exists"
    fi    
}
