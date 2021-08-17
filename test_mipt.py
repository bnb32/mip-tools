from miptools import *
import netCDF4 as nc

modelDict=setFileDictFields(base_dir="/data/GCM",project="CMIP5",
                            variable="pr",cmor_table="Amon",
                            output_type="fullpath")



dotStr='/data/GCM.CMIP5.historical.Amon.pr.GISS-E2-R.r1i1p1.*.*'
md=parseDotStr(dotStr)
f=getmodelinfo(md,output_type="file")
D=nc.MFDataset(md["dir"]+md["file_pattern"])


