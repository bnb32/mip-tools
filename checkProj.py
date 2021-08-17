#!/usr/bin/env python 

import sys
import os
import json
import miptools as manager

echoMode=False

print(sys.executable)
#rootDataDir="/Users/tra38/projects/NMME-SIx-devel/data/scratch/" #myPyParams.pathToBabylon0
#print(sys.argv[0])

srcDir=sys.argv[1]
#srcDir="/Users/tra38/projects/NMME-SIx-devel/data/scratch/source/"#rootDataDir+"Reforecasts/tra38/scratch/src/" #place where stuff is now

targetDir=sys.argv[2]
#targetDir="/Users/tra38/projects/NMME-SIx-devel/data/scratch/target/"#rootDataDir+"Reforecasts/tra38/scratch/target/"#target directory where things will end up

print(srcDir)
print(targetDir)

for root, dirs, files in os.walk(srcDir):
    for f in files:
        fullFileNameWithPath = os.path.join(root, f)

        if(os.path.splitext(fullFileNameWithPath)[1] == '.nc'):
            print("-----------------------------------------------------------------")
            print("Now processing: "+fullFileNameWithPath)

            
            startDate,endDate=manager.getDateEdgesFromFile(fullFileNameWithPath)
            fileInfoDict=manager.fileName2FileInfoDict(fullFileNameWithPath)                    

                
                

                
            
