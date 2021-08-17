#!/usr/bin/env python

#from joblib import Parallel,delayed
import multiprocessing
import subprocess
import sys

sys.path.append("../")

from ret_tools import par_run

MODELS=[]
EXPERIMENTS=[]

def compute_pdsi(model,exp):
    #call pdsi code here
    #subprocess.call([])

for MODEL in MODELS:
    for EXP in EXPERIMENTS:
        par_run(compute_pdsi,MODEL,EXP)

#Parallel(n_jobs=(len(MODELS)*len(EXPERIMENTS))(delayed(compute_pdsi)(MODEL) for MODEL in model_list)    
