import os, sys, glob
from os import path
import numpy as np
import socket,string, yaml
import netCDF4 as nc
from string import Template
from datetime import datetime, timedelta
import cftime as cf

'''
Ojects should be:
    - Run
        Run.files
    - Ensemble 

Dictionaries should be:
    - fileDict
    - columnDct

'''

def yaml2dict(yaml_file):
    with open(yaml_file,'r') as f:
        yaml_dict=yaml.load(f)
    return(yaml_dict)

def dict2yaml(yaml_dict,yaml_file,flw_sty=False):
    '''dict2yaml(yaml_dict,yaml_file,default_flow_style=False)'''
    with open(yaml_file,'w') as f:
        yaml.dump(yaml_dict,f,default_flow_style=flw_sty)

file_dict=yaml2dict("dictionaries/run_fields.yaml")

def setup_file_dict(file_dict=file_dict, dot_str=None):
    new_file_dict=file_dict.copy()
    md=parseDotStr(dot_str)
    for k in md.keys():
        new_file_dict[k]=md[k]
    return(new_file_dict)


def dict2sql_entry(file_dict,colNames):                
    entryDict=dict()
    for cols in colNames:
        entryDict[cols]=file_dict[cols]
    colStr=','.join(colNames)
    INSRT_CMMND='INSERT INTO %TABLENAME% ('+colStr+')'
    ENTRIES=tuple(entryDict.values)
    VALS_CMMND='VALUES ('+'?,'*(len(colNames)-1)+'?)'
    return(INSRT_CMMND,VALS_CMMND,ENTRIES)

#setup a "climate data library" (CDL)
class CDL:
    @classmethod
    def __init__(self,dot_str=None,input_dict=None):
        init_dict=yaml2dict("dictionaries/run_fields.yaml")
        if input_dict is None and dot_str is None:            
            print("Initializing empty climate data library")            
        elif input_dict is not None and dot_str is None:
            print("Initializing input_dict from input")
            for k in input_dict.keys():
                init_dict[k]=input_dict[k]
        elif input_dict is None and dot_str is not None:
            str_dict=parse_dot_str(dot_str)
            for k in str_dict.keys():
                init_dict[k]=str_dict[k]
        elif input_dict is not None and dot_str is not None:
            raise ValueError("either input_dict or dot_str may be set, but noth both")
        
        getmodelinfo(init_dict,output_type="exist")
        self.file_dict=init_dict
        for k in self.file_dict.keys():
            setattr(self,k,self.file_dict[k])
            
    @classmethod
    def update(self):
        for k in self.file_dict.keys():
            setattr(self,k,self.file_dict[k])
            
    @classmethod
    def append_attrs(self,new):
        for k in new.keys():
            setattr(self,k,new[k])

class Ensemble(CDL):
    @classmethod
    def __init__(self,dot_str=None,input_dict=None):
        self=CDL(dot_str,input_dict)
        (ens,eroot)=getEnsIDs(self.file_dict)
        self.file_dict["ensemble_list"]=ens
        self.file_dict["ensemble_root"]=eroot
        self.update()

class Member(CDL):
    @classmethod
    def add_date_info(self,**kwargs):        
        try:
            sStr,eStr,nt=getDateEdgesFromFlist(self.file_dict["flist"])
            dInfo=buildDateEdgeInfoDict(sStr,eStr)
            self.file_dict["startDateStr"]=sStr
            self.file_dict["endDateStr"]=eStr
            self.file_dict["nTime"]=nt
            copyDateInfoDict(dInfo,self.file_dict)
            self.update()
        except:
            print("warning: failed to find end dates")

    @classmethod
    def import_data(self,lonEdges=(),latEdges=(),timeEdges=()):
        if len(self.file_dict["flist"]) == 0:
            print("No data to import")
        if len(self.file_dict["flist"]) == 1:
            self.ncDataset=nc.Dataset(self.file_dict["flist"][0])
        if len(self.file_dict["flist"]) >1:
            self.ncDataset=nc.MFDataset(self.file_dict["fullpath"])

        



def parse_dot_str(dotStr):
    '''Strings should be constructed like this:

    [ROOT_DIR].[proj].[exp].[Ctable].[var].[mod].[ens].[dStart].[dEnd]

    ROOT_DIR: base directory of project
    proj:     project (CMIP5, CMIP6, LENS, BRACE, etc...)
    exp:      experiment (historial, piControl, past1000, etc...)
    Ctable:   cmor_table (Amon, Omon, Lmon, Aday, etc...)
    ens:      ensemble (r1i1p1, run1, 01, etc...)
    dStart:   start date (YYYYMM or YYYYMMDD)
    dEnd:     end date (YYYYMM or YYYYMMDD)


    dotStr='/data/GCM.CMIP5.historical.Amon.pr.GISS-E2-R.r1i1p1.*.*'
                    [0]   [1]        [2]  [3] [4]      [5]   [6]
    md=parseDotStr(dotStr)
    '''

    dotlist=dotStr.split('.')
    md=setFileDictFields()
    md["base_dir"]=dotlist[0]
    md["project"]=dotlist[1]
    md["experiment"]=dotlist[2]
    md["cmor_table"]=dotlist[3]
    md["variable"]=dotlist[4]
    md["model"]=dotlist[5]
    md["ensemble"]=dotlist[6]
    md["startDateStr"]=dotlist[7]
    md["endDateStr"]=dotlist[8]

    return(md)

def buildDateEdgeInfoDict(startDateStr,endDateStr):
    dateInfoDict=dict()

    if not startDateStr=="*" and not endDateStr=="*":
        dateInfoDict["startDateStr"]=startDateStr
        dateInfoDict["endDateStr"]=endDateStr
        dateInfoDict["startDate"]=dateStr2Date(startDateStr)
        dateInfoDict["endDate"]=dateStr2Date(endDateStr)
        s,e,t=dateEdgesAsInt(startDateStr,endDateStr)
        dateInfoDict["startYear"]=s[0]
        dateInfoDict["startMo"]=s[1]
        dateInfoDict["endYear"]=e[0]
        dateInfoDict["endMo"]=e[1]
    else:
        dateInfoDict={'startDateStr':startDateStr,'endDateStr':endDateStr,
                      'startDate':None,'endDate':None,
                      'startYear':None,'startMo':None,
                      'endYear':None,'endMo':None}


    return(dateInfoDict)

def copyDateInfoDict(dInfo,md):
    for k in dInfo.keys():
        md[k]=dInfo[k]

def getDateInfo(md,**kwargs):
    sStr=md["startDateStr"]
    eStr=md["endDateStr"]
    dInfo=buildDateEdgeInfoDict(sStr,eStr)                       
    copyDateInfoDict(dInfo,md)
        

def dateStr2Date(dateStr,fmt='%Y%m'):
    d=datetime.strptime(dateStr,fmt)
    return(d)

def dateStrYYYYMM2Int(dateStr):
    year=int(dateStr[0:4])
    mo=int(dateStr[-2:])
    return(year,mo)

def dateEdgesAsInt(startDateStr,endDateStr):
    s=dateStrYYYYMM2Int(startDateStr)
    e=dateStrYYYYMM2Int(endDateStr)
    dateEdgeInts=(s[0],s[1],e[0],e[1])
    return s,e,dateEdgeInts

def getDateEdgesFromFlist(fullFlist,timeVarName="time",fmt='%Y%m'):
    D=nc.MFDataset(fullFlist)
    time=nc.MFTime(D.variables[timeVarName])
    nt=len(time)
    pseudoDates=cf.num2date(time[:],units=time.units,calendar=time.calendar,
                            only_use_cftime_datetimes=True)

    startDateStr=cf.datetime.strftime(pseudoDates[0],fmt).replace(' ','0')#hack!
    endDateStr=cf.datetime.strftime(pseudoDates[-1],fmt).replace(' ','0')
    D.close()
    return startDateStr,endDateStr,nt

def getDateEdgesFromFile(fullFileName,timeVarName="time",fmt='%Y%m'):
    D=nc.Dataset(fullFileName)
    time=D.variables[timeVarName]
    pseudoDates=cf.num2date(time[:],units=time.units,calendar=time.calendar,
                            only_use_cftime_datetimes=True)
#    print(time.calendar)

    startDateStr=cf.datetime.strftime(pseudoDates[0],fmt)
    endDateStr=cf.datetime.strftime(pseudoDates[-1],fmt)
    D.close()
    return startDateStr,endDateStr


def fileName2FileInfoDict(fullFileName,fmt="%Y%m"):
    fileInfoDict=setFileDictFields();

    fileParts=fullFileName.split("/")[-1].split("_")
    fileInfoDict["variable"]=fileParts[0]
    fileInfoDict["cmor_table"]=fileParts[1]
    fileInfoDict["model"]=fileParts[2]
    fileInfoDict["experiment"]=fileParts[3]
    fileInfoDict["ensemble"]=fileParts[4].split(".")[0]
    fileInfoDict["startDateStr"]=fileParts[-1].split("-")[0]
    fileInfoDict["endDateStr"]=fileParts[-1].split("-")[-1].split('.')[0]    
    fileInfoDict["fileSuffix"]=fileParts[-1]
        
    
    if fileInfoDict["realm"]=="Ayear":
        fmt="%Y"
    elif fileInfoDict["realm"]=="Amon":
        fmt="%Y%m"
    elif fileInfoDict["realm"]=="Aday":
        fmt="%Y%m%d"
    elif fileInfoDict["realm"]=="year":
        fmt="%Y"
    elif fileInfoDict["realm"]=="mon":
        fmt="%Y%m"
    elif fileInfoDict["realm"]=="day":
        fmt="%Y%m%d"
    elif fileInfoDict["realm"]=="Oyear":
        fmt="%Y"
    elif fileInfoDict["realm"]=="Omon":
        fmt="%Y%m"
    elif fileInfoDict["realm"]=="Oday":
        fmt="%Y%m%d"
    elif fileInfoDict["realm"]=="Lyear":
        fmt="%Y"
    elif fileInfoDict["realm"]=="Lmon":
        fmt="%Y%m"
    elif fileInfoDict["realm"]=="Lday":
        fmt="%Y%m%d"


    fileInfoDict["fmt"]=fmt
    fileInfoDict["originalName"]=fullFileName
                  
    return fileInfoDict

def setFileDictFields(mdin=dict(),**kwargs):
    """
    ex:
    modelDict=setFileDictFields(base_dir="/data/GCM",project="CMIP5",
                                variable="pr",cmor_table="Amon",
                                experiment="historical",
                                ensemble="r1i1p1",model="CCSM4",
                                output_type="fullpath")
    """
    md=dict(realm="*",project="*",product="*",model="*",variable="*", version="*",
            experiment="*",time_frequency="*",institute="*",ensemble="*",
            index_node="*", cmor_table="*",
            base_dir="*",startDateStr="*",endDateStr="*", exist="unkown")
    
    for key in mdin.keys():
        md[key]=mdin[key]

    for key in kwargs.keys():
        md[key]=kwargs[key]

    return(md)

def modeldict2fname(md):
    '''filename=modeldict2fname(md)'''
    file_fmt="%s_%s_%s_%s_%s_%s-%s.nc"
    filename= file_fmt % (md["variable"],md["cmor_table"],md["model"],
                          md["experiment"],md["ensemble"],md["startDateStr"],
                          md["endDateStr"])
    return(filename)

def modeldict2dir(md):
    '''dirname=modeldict2dir(md)'''
    dir_fmt="%s/%s/%s/%s/%s/%s/%s/"
    dirname= dir_fmt % (md["base_dir"],md["project"],md["experiment"],
                        md["cmor_table"],md["variable"],md["model"],
                        md["ensemble"])
    return(dirname)

def getEnsIDs(md,**kwargs):
    df = "%s/%s/%s/%s/%s/%s" 
    md_root = df % (md["base_dir"],md["project"],md["experiment"],
                    md["cmor_table"],md["variable"],md["model"])
    try:
        ensIDs=os.listdir(md_root)
    except:
        ensIDs=None

    return(ensIDs,md_root)
def getmodelinfo(md,**kwargs):
    for ks in kwargs.keys():
        md[ks]=kwargs[ks]


    f=modeldict2fname(md)
    d=modeldict2dir(md)
    flist=glob.glob(d+f)
    md["file_pattern"]=f
    md["fullpath"]=d+f
    md["dir"]=d
    md["flist"]=flist
    md["files"]=" ".join(flist)
    if len(flist) > 0:
        md["exist"]="true"
        
        if md["output_type"] == "file":
            strOut=md["file_pattern"]
        elif md["output_type"] == "dir":
            strOut=md["dir"]
        elif md["output_type"] == "fullpath":
            strOut=md["fullpath"]
        elif md["output_type"] == "exist":
            strOut=md["exist"]
        elif md["output_type"] == "flist":
            strOut=""
            if len(flist) == 0:
                strOut = "false"
            elif len(flist) > 1:
                for i in range(len(flist)):
                    strOut=strOut+" "+flist[i]

            elif len(flist) == 1:
                strOut=flist[0]

        else:
            strOut=None
        
        return(strOut)


