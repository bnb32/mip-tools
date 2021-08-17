#!/bin/env python

import os, sys, argparse, textwrap, glob
from os import path
from miptools import getmodelinfo, modeldict2fname, modeldict2dir, setupModInfo

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Return expected file name for CMIP5-conforming file from input",
    epilog=textwrap.dedent('''\n  Examples (-otype specifies what kind of output is returned): \n'''
                           '   Directory name only: \n' 
                           '     '+sys.argv[0]+''' -otype dir -base_dir /data/GCM -p CMIP5 -var pr  -c Amon -ex historical -en r1i1p1 -m CCSM4 \n'''
                           '   File name: \n' 
                           '     '+sys.argv[0]+''' -otype file -base_dir /data/GCM -p CMIP5 -var pr -c Amon -ex historical -en r1i1p1 -m CCSM4 \n'''
                           '   Full path (all files): \n' 
                           '     '+sys.argv[0]+''' -otype fullpath -base_dir /data/GCM -p CMIP5 -var pr  -c Amon -ex historical -en r1i1p1 -m CCSM4 \n'''
                           '   Just check if files exist (returns string "true" or "false"): \n' 
                           '     '+sys.argv[0]+''' -otype exist -base_dir /data/GCM -p CMIP5 -var pr -c Amon -ex historical -en r1i1p1 -m CCSM4 \n'''
                           '   List all files for search (note: * must be quoted as "*"): \n' 
                           '     '+sys.argv[0]+''' -otype flist -base_dir /data/GCM -p CMIP5 -var pr -c Amon -ex historical -en r1i1p1 -m CCSM4 \n'''
                           '     '+sys.argv[0]+''' -otype flist -base_dir /data/GCM -p CMIP5 -var pr -c Amon -ex historical -en "*" -m CCSM4 \n'''
                           '     '+sys.argv[0]+''' -otype flist -base_dir /data/GCM -p CMIP5 -var pr -c Amon -ex "*" -en "*" -m CCSM4 \n'''))
parser.add_argument('-r', dest='realm', nargs='?', default='*', const=True)
parser.add_argument('-p', dest='project', nargs='?', default='*',const=True)
parser.add_argument('-prod', dest='product', nargs='?', default='*', const=True)
parser.add_argument('-m', dest='model', nargs='?', default='*', const=True)
parser.add_argument('-var', dest='variable', nargs='?', default='*', const=True)
parser.add_argument('-ver', dest='version', nargs='?',default='*', const=True)
parser.add_argument('-ex', dest='experiment', nargs='?', default='*',const=True)
parser.add_argument('-t', dest='time_frequency', nargs='?', default='*',const=True)
parser.add_argument('-i', dest='institute', nargs='?', default='*',const=True)
parser.add_argument('-en', dest='ensemble', nargs='?', default='*',const=True)
parser.add_argument('-in', dest='index_node', nargs='?', default='*',const=True)
parser.add_argument('-id', dest='id', nargs='?', default='*',const=True)
parser.add_argument('-c', dest='cmor_table', nargs='?', default='*',const=True)
parser.add_argument('-dStart', dest='dateStart', nargs='?', default='*',const=True)
parser.add_argument('-dEnd', dest='dateEnd', nargs='?', default='*',const=True)
parser.add_argument('-base_dir', dest='base_dir', nargs='?', default='.',const=True)
parser.add_argument('-exist', dest='exist', nargs='?', default='false',const=True)
parser.add_argument('-otype', dest='output_type', nargs='?', default='file',const=True)

args = parser.parse_args()
args_dict = vars(args)

md=args_dict

strOut=getmodelinfo(md)
print(strOut)

