#!/usr/bin/env python

# modules

import argparse
import sys,subprocess,os
import json
import numpy as np
import textwrap
import threading
import multiprocessing
from ret_tools import *

# env variables

curr_dir=os.path.dirname(os.path.abspath(__file__))
data_dir = curr_dir+"/data"
cv_dir = curr_dir+"/CMIP6_CVs"
dict_dir = curr_dir+"/dictionaries"
data_node="https://esgf-node.llnl.gov"
fetch_url=data_node+"/esg-search/wget?"
query_fmt = data_node+"/esg-search/search?replica=false&latest=true&sort=true&format=application%2Fsolr%2Bjson"

# argument parsing

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Retrieves data from ESGF according to optional parameter values. Use the '-q' flag to print out results which match specified values",
    epilog=textwrap.dedent('''\
                           download example: '''+sys.argv[0]+''' CMIP6 -var tas -r atmos -t mon -ex historical
                           query example: '''+sys.argv[0]+''' CMIP6 -q -r atmos -t mon -ex -en -i -m'''))
parser.add_argument('-q', dest='query', action='store_true', help="query valid parameters sets with output specified by included flags")
parser.add_argument('project', nargs='?', help="required input e.g. CMIP6, CMIP5, etc")
parser.add_argument('-l', dest='limit', nargs='?', type=int, help="number of query outputs")
parser.add_argument('-o', dest='offset', nargs='?', type=int, help="start number of query outputs")
parser.add_argument('-r', dest='realm', nargs='?', const=True, default=True)
parser.add_argument('-prod', dest='product', nargs='?', const=True)
parser.add_argument('-var', dest='variable', nargs='?', const=True)
parser.add_argument('-ver', dest='version', nargs='?', const=True)
parser.add_argument('-in', dest='index_node', nargs='?', const=True, help="base url for data")
parser.add_argument('-id', dest='id', nargs='?', const=True)
parser.add_argument('-d', dest='data_dir', nargs='?', const=True, default=data_dir, help="specify full path for data directory. default is ./data")

## diff names for pre cmip6
parser.add_argument('-m', dest='source_id', nargs='?', const=True, help="model id")
parser.add_argument('-ex', dest='experiment_id', nargs='?', const=True, default=True)
parser.add_argument('-t', dest='frequency', nargs='?', const=True, help="time frequency")
parser.add_argument('-i', dest='institution_id', nargs='?', const=True)
parser.add_argument('-en', dest='member_id', nargs='?', const=True, default=True, help="ensemble id")
parser.add_argument('-c', dest='table_id', nargs='?', const=True)
parser.add_argument('-res', dest='nominal_resolution', nargs='?', const=True)
parser.add_argument('-g', dest='grid', nargs='?', const=True)
parser.add_argument('-gl', dest='grid_label', nargs='?', const=True)
##

args=parser.parse_args()
args_dict = vars(args)

if (args.project != "CMIP6"):
    args_dict['model']=args_dict['source_id']
    args_dict['experiment']=args_dict['experiment_id']
    args_dict['time_frequency']=args_dict['frequency']
    args_dict['institute']=args_dict['institution_id']
    args_dict['ensemble']=args_dict['member_id']
    args_dict['cmor_table']=args_dict['table_id']
    del args_dict['source_id']
    del args_dict['experiment_id']
    del args_dict['frequency']
    del args_dict['institution_id']
    del args_dict['member_id']
    del args_dict['table_id']
    del args_dict['nominal_resolution']
    del args_dict['grid']
    del args_dict['grid_label']

# vocabulary dictionaries
dictionaries={}

if args.project=="CMIP6":

    dictionaries['realm']=json.load(open(cv_dir+"/CMIP6_realm.json","r"))["realm"] 
    dictionaries['frequency']=json.load(open(cv_dir+"/CMIP6_frequency.json","r"))["frequency"] 
    dictionaries['institution_id']=json.load(open(cv_dir+"/CMIP6_institution_id.json","r"))["institution_id"] 
    dictionaries['source_id']=json.load(open(cv_dir+"/CMIP6_source_id.json","r"))["source_id"] 
    dictionaries['table_id']=json.load(open(cv_dir+"/CMIP6_table_id.json","r"))["table_id"] 
    dictionaries['experiment_id']=json.load(open(cv_dir+"/CMIP6_experiment_id.json","r"))["experiment_id"] 

else:

    dictionaries['realm']=json.load(open(dict_dir+"/realm.json","r"))["realm"]
    dictionaries['project']=json.load(open(dict_dir+"/project.json","r"))["project"] 
    dictionaries['time_frequency']=json.load(open(dict_dir+"/time_frequency.json","r"))["time_frequency"] 
    dictionaries['institute']=json.load(open(dict_dir+"/institute.json","r"))["institute"] 
    dictionaries['product']=json.load(open(dict_dir+"/product.json","r"))["product"] 
    dictionaries['model']=json.load(open(dict_dir+"/model.json","r"))["model"] 
    dictionaries['variable']=json.load(open(dict_dir+"/variable.json","r"))["variable"] 
    dictionaries['version']=json.load(open(dict_dir+"/version.json","r"))["version"] 
    dictionaries['cmor_table']=json.load(open(dict_dir+"/cmor_table.json","r"))["cmor_table"] 
    dictionaries['index_node']=json.load(open(dict_dir+"/index_node.json","r"))["index_node"] 
    dictionaries['ensemble']=json.load(open(dict_dir+"/ensemble.json","r"))["ensemble"] 
    dictionaries['experiment']=json.load(open(dict_dir+"/experiment.json","r"))["experiment"] 

# query

if not args.limit: args.limit=10;
if not args.offset: args.offset=0;

query_url = query_fmt+"&limit="+str(args.limit)+"&offset="+str(args.offset)+"&fields="
script_name="fetch"

script_name=get_wget_script(args,args_dict,dictionaries,query_url,fetch_url,script_name,args.data_dir)    
# run download script

openid="https://esgf-node.llnl.gov/esgf-idp/openid/ecrl-user"
password="ESG let me in 2018!"

run_wget_script(args.data_dir,script_name,openid,password)
#print(child)
