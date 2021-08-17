#babylonFileManager.py
"""
Created on Fri Jul  3 10:21:13 2015

@author: tra38
"""

import numpy as np
import socket,string
import netCDF4 as nc
from string import Template
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num
import cftime as netcdftime

########################################################################
hostname=socket.gethostname()
if hostname == 'AG-EAS-7E0FD57.local':
    pathToBabylon0='/Volumes/data/'    
elif hostname == 'ag-eas-bluesky.eas.cornell.edu':
    pathToBabylon0='/data/'
elif hostname == 'ag-eas-monsoon.eas.cornell.edu':
    pathToBabylon0='/data/'



    
################### Dictionaries ########################################

knownVarNames={'time':'time',
               'TIME':'time',
               'lon':'lon',
               'LON':'lon',
               'long':'lon',               
               'longitude':'lon',
               'lat':'lat',
               'LAT':'lat',
               'latitude':'lat',
               'tasmax':'tasmax',
               'tasmin':'tasmin',
               'pr':'pr',
               'prate':'pr',
               'precip':'pr',
               'precipitation':'pr'}

knownDimNames={'time':'time',
               'TIME':'time',
               'lon':'lon',
               'LON':'lon',
               'long':'lon',               
               'longitude':'lon',
               'lat':'lat',
               'LAT':'lat',
               'latitude':'lat'}
########################################################################               
def renameDimsVarsToLower(fullFileName):
    '''Re-writes variable names and dimension of a netcdf file
    ('fullFileName') to lower case.'''

    f=nc.Dataset(fullFileName,"a")    
    for var in f.variables:
        if var != string.lower(var):
            print('renaming variable "'+var+'" in file "'+fullFileName+' to "'+ string.lower(var)+ '"')
            f.renameVariable(var,string.lower(var))

    for dim in f.dimensions:
        if dim != string.lower(dim):
            print('renaming dimension "'+dim+'" in file "'+fullFileName+' to "'+ string.lower(dim)+ '"')
            f.renameDimension(dim,string.lower(dim))

    f.close()
        

def setFileDictFields(varName="",realm="",modID="",expID="",ensID="",startDate="",endDate="",fileSuffix="",originalName=""):
    return locals()

def getDatesFromFile(fullFileName,timeVarName="time",fmt='%Y%m%d'):
    ncHandle=nc.Dataset(fullFileName)
    time=ncHandle.variables[timeVarName]
    pseudoDates=num2date(time[:],units=time.units,calendar=time.calendar)
    print(time.calendar)

    # firt try with  datetime, which is the default:
    try:
        startDate=datetime.strftime(pseudoDates[0],fmt)
        endDate=datetime.strftime(pseudoDates[-1],fmt)
        
    # then do use netcdftime strfime if that fails:    
    except: 
        startDate=netcdftime.datetime.strftime(pseudoDates[0],fmt)
        endDate=netcdftime.datetime.strftime(pseudoDates[-1],fmt)
        
    return startDate,endDate

def fileName2FileInfoDict(fullFileName):
    fileInfoDict=setFileDictFields();

    fileParts=fullFileName.split("/")[-1].split("_")
    fileInfoDict["varName"]=fileParts[0]
    fileInfoDict["realm"]=fileParts[1]
    fileInfoDict["modID"]=fileParts[2]
    fileInfoDict["expID"]=fileParts[3]
    fileInfoDict["ensID"]=fileParts[4].split(".")[0]
    fileInfoDict["startDate"]=fileParts[-1].split("-")[0]
    fileInfoDict["endDate"]=fileParts[-1].split("-")[-1].split('.')[0]    
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

def fileInfoDict2FileName(fileInfoDict):
    #varName_realm_modID_expID_ensID_startDate-EndDate.nc
    file_template=Template("""${varName}_${realm}_${modID}_${expID}_${ensID}_${startDate}-${endDate}.${fileSuffix}""")    
    fileName=file_template.substitute(fileInfoDict)    
    return fileName

def fileInfoDict2PathName(fileInfoDict):
    #... expID/realm/varName/modID/ensID/
    
    folder_template=Template("""${expID}/${realm}/${varName}/${modID}/${ensID}/""")
    pathName=folder_template.substitute(fileInfoDict)    
    return pathName

def checkFileName(fileName):
    legitName=False
    fileInfo=fileName.split('_')    
    if len(fileInfo) == 6: #check at least first few parts are there:
        if len(fileInfo[-1].split('-'))==2:
            if(fileInfo[-1].split('.')[-1]=='nc' or fileInfo[-1].split('.')[-1]=='nc4'):
                legitName = True
            
    return legitName              

def checkPartialFileName(fileName):
    legitName=False
    fileInfo=fileName.split('_')    
    if len(fileInfo) >= 5: #check at least first few parts are there:
        if(fileInfo[-1].split('.')[-1]=='nc' or fileInfo[-1].split('.')[-1]=='nc4'):
            legitName = True

    return legitName              


