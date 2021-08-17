#!/bin/env python
import sqlite3 as sqlite
import os
import miptools as mpt
from miptools import yaml2dict,dict2yaml


file_dict_tmplt=mpt.setFileDictFields(yaml2dict("dictionaries/run_fields.yaml"),
                                      startDateStr="*",endDateStr="*")

print("/scenario/Realm/variable/MODEL/ensemble/")
print("variable_Realm_MODEL_scenario_ensemble_YYYYMM-YYYYMM")
dbPath="/data2/tra38/shared_projects/lim-corr/db"
dbFile='babylon0.db'
dbFullName=dbPath+"/"+dbFile
rmDB=True

if rmDB and os.path.isfile(dbFullName):
    os.remove(dbFullName)


columns={'project':'TEXT','variable':'TEXT','cmor_table':'TEXT',
         'model':'TEXT','exist':'TEXT','imported':'TEXT',
         'experiment':'TEXT','ensemble':'TEXT',
         'startDateStr':'TEXT', 'endDateStr':'TEXT', 
         'startYear':'INTEGER', 'startMo':'INTEGER',
         'endYear':'INTEGER','endMo':'INTEGER',
         'startDate':'DATETIME','endDate':'DATETIME',
         'nTime':'INTEGER','file_pattern':'TEXT',
         'files':'TEXT','fullpath':'TEXT'}

colNames=columns.keys()

projects={'CMIP5':'CMIP5'} #it is required to include a comma when specifying a tuple with only one element
base_dirs={'CMIP5':'/data/GCM'}
expIDs=('historical','past1000','piControl','rcp26','rcp45','rcp60','rcp85')
#expIDs=('historical',)
varIDs={'Amon':('pr','ps','huss','rlds','rlus','rsds','rsus','tas'),'Lmon':('mrso',)}
#varIDs={'Amon':('pr',),'Lmon':('mrso',)}
modIDs=('ACCESS1-0','BNU-ESM','CESM1-BGC','CESM1-WACCM',
        'CNRM-CM5','EC-EARTH', 'GFDL-CM3', 'GISS-E2-H-CC',
        'HadGEM2-AO', 'IPSL-CM5A-LR' , 'MIROC5', 'MPI-ESM-MR' ,
        'NorESM1-M', 'ACCESS1-3' , 'CanCM4' , 'CESM1-CAM5' ,
        'CMCC-CESM', 'CNRM-CM5-2', 'FGOALS-g2', 'GFDL-ESM2G',
        'GISS-E2-R', 'HadGEM2-CC', 'IPSL-CM5A-MR', 'MIROC-ESM',
        'MPI-ESM-P', 'NorESM1-ME', 'bcc-csm1-1', 'CanESM2',
        'CESM1-CAM5-1-FV2', 'CMCC-CM', 'CSIRO-Mk3-6-0', 'FIO-ESM',
        'GFDL-ESM2M', 'GISS-E2-R-CC', 'HadGEM2-ES', 'IPSL-CM5B-LR',
        'MIROC-ESM-CHEM', 'MRI-CGCM3', 'bcc-csm1-1-m', 'CCSM4',
        'CESM1-FASTCHEM', 'CMCC-CMS', 'CSIRO-Mk3L-1-2', 'GFDL-CM2p1',
        'GISS-E2-H', 'HadCM3', 'inmcm4', 'MIROC4h', 'MPI-ESM-LR',
        'MRI-ESM1')

cmor_tables=varIDs.keys()

INIT_CMMND=''
for cnames in columns.keys():
    INIT_CMMND=INIT_CMMND+cnames+' '+columns[cnames]+', '        

db=sqlite.connect(dbFullName)
cur=db.cursor()
for p in projects.keys():
    TABLENAME=projects[p]
    SQ_CMMND='CREATE TABLE '+TABLENAME+'('+ INIT_CMMND[0:-2]+')' 

    cur.execute(SQ_CMMND)
    for e in expIDs:
        for c in cmor_tables:
            vars=varIDs[c]
            for v in vars:
                for m in modIDs:
                    
                    md=mpt.setFileDictFields(file_dict_tmplt,base_dir=base_dirs[p],
                                             project=projects[p], variable=v,
                                             experiment=e, cmor_table=c, model=m,
                                             output_type="file_pattern",
                                             imported="false",startDateStr="*",
                                             endDateStr="*")
                                             
                    mpt.getmodelinfo(md)
                    print(md["fullpath"])
                    ensembleIDs,md_root=mpt.getEnsIDs(md)
                    if ensembleIDs is None:
                        mdf0=md.copy()
                        entryDict=dict()
                        for cols in colNames:
                            entryDict[cols]=mdf0[cols]

                        onESG="unknown"
                        INSRT_CMMND='INSERT INTO '+TABLENAME +' ('+','.join(colNames)+')'
                        ENTRIES=tuple(entryDict.values())
                        VALS_CMMND='VALUES ('+'?,'*(len(colNames)-1)+'?)'

                        cur.execute(INSRT_CMMND+VALS_CMMND,ENTRIES)

                    else:
                        for ens in ensembleIDs:
                            mdf0=md.copy()
                            mdf0["ensemble"]=ens
                            mpt.getmodelinfo(mdf0,output_type="exist")
                            if mdf0["exist"]=="true":
                                try:
                                    mdf0["startDateStr"],mdf0["endDateStr"], mdf0["nTime"]=mpt.getDateEdgesFromFlist(mdf0["fullpath"])
                                    mdf0["imported"]="true"
                                    print("Successfully read time of: " + mdf0["fullpath"])
                                except:
                                    print("Failed to read time of: " + mdf0["fullpath"])
                            else:
                                print("Failed to find files for: " + mdf0["fullpath"])
                                

                            mpt.getDateInfo(mdf0)
                            entryDict=dict()
                            for cols in colNames:
                                entryDict[cols]=mdf0[cols]

                            onESG="unknown"
                            INSRT_CMMND='INSERT INTO '+TABLENAME +' ('+','.join(colNames)+')'
                            ENTRIES=tuple(entryDict.values())
                            VALS_CMMND='VALUES ('+'?,'*(len(colNames)-1)+'?)'

                            cur.execute(INSRT_CMMND+VALS_CMMND,ENTRIES)



db.commit()
db.close()

os.system("chmod -R 775 " + dbFullName)
