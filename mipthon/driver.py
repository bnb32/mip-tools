#!/usr/bin/env python

import os,sys
import subprocess
import multiprocessing
import re

sys.path.append("../")
from ret_tools import par_run


#ROOT_DIR="/data/team/cmip6/pdsi/"
ROOT_DIR="/data/team/bnb32/test"

VMIP="CMIP6"
MODELS=["MRI-ESM2-0"];
#EXPERIMENTS=["historical", "ssp119", "ssp585"]
EXPERIMENTS=["historical"]
FREQUENCIES=["mon"];
#VARIABLES=["pr", "tasmin", "tasmax", "vas", "uas", "rlds", "rlus", "rsds", "rsus", "zg"];
VARIABLES=["pr"];

DATA_DIR="%s/%s/%s/%s/%s/%s/"

def nc_download(vmip,model,exp,freq,var,rdir):
    dir=DATA_DIR %(rdir,vmip,model,exp,freq,var)
    subprocess.call(["python","../retriever.py",vmip,"-m",model,"-ex",exp,"-t",freq,"-var",var,"-d",dir])

for MODEL in MODELS:
    for EXP in EXPERIMENTS:
        for FREQ in FREQUENCIES:
            for VAR in VARIABLES:
                par_run(nc_download,VMIP,MODEL,EXP,FREQ,VAR,ROOT_DIR)
                #dl_thread=multiprocessing.Process(target=nc_download,args=(VMIP,MODEL,EXP,FREQ,VAR,ROOT_DIR));
                #dl_thread.start()
