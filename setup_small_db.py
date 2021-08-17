#!/bin/env python
import sqlite3 as sqlite
import os
import miptools as mpt
from miptools import yaml2dict, dict2yaml
import yaml
from os.path import join

print("/scenario/Realm/variable/MODEL/ensemble/")
print("variable_Realm_MODEL_scenario_ensemble_YYYYMM-YYYYMM")

templates_dir="dictionaries"
colTemplateFile="db_columns.yaml"
colTmplt=join(templates_dir,colTemplateFile)

runTemplateFile="run_fields.yaml"
runRunTmplt=join(templates_dir,runTemplateFile)

dbPath="/data2/tra38/shared_projects/lim-corr/db"
dbFile='babylon0_light.db'
dbFullName=join(dbPath,dbFile)
rmDB=True
if rmDB and os.path.isfile(dbFullName):
    os.remove(dbFullName)

columns=yaml2dict(colTmplt)
colNames=columns.keys()

projects={'CMIP5':'CMIP5'} #it is required to include a comma when specifying a tuple with only one element
base_dirs={'CMIP5':'/data/GCM'}
#expIDs=('historical',)'past1000','piControl','rcp26','rcp45','rcp60','rcp85')
expIDs=('historical',)
#varIDs={'Amon':('pr','ps','huss','rlds','rlus','rsds','rsus','tas'),'Lmon':('mrso',)}
varIDs={'Amon':('pr',),'Lmon':('mrso',)}
modIDs=('ACCESS1-0','BNU-ESM','CESM1-BGC','CESM1-WACCM')

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
                    
                    md=mpt.setFileDictFields(base_dir=base_dirs[p],
                                             project=projects[p],
                                             variable=v,experiment=e,
                                             cmor_table=c, model=m,
                                             output_type="file_pattern",
                                             imported="false",nTime=None)
                    mpt.getmodelinfo(md)
                    print(md["fullpath"])
                    ensembleIDs,md_root=mpt.getEnsIDs(md)
                    if ensembleIDs is None:
                        mdf0=md.copy()
                        mdf0["exist"]="false"
                        mdf0["nTime"]=None
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
                                    mdf0["startDateStr"],mdf0["endDateStr"],mdf0["nTime"]=mpt.getDateEdgesFromFlist(mdf0["fullpath"])
                                    mdf0["imported"]="true"
                                    print("Successfully read time of: " + mdf0["fullpath"])
                                except:
                                    mdf0["imported"]="false"
                                    mdf0["nTime"]=None
                                    print("Failed to read time of: " + mdf0["fullpath"])
                            else:
                                mdf0["imported"]="false"
                                mdf0["nTime"]=None
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
