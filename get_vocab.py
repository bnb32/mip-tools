#!/bin/python

import argparse
import sys,subprocess,os
import json,urllib
import numpy as np
import textwrap
import re

data_node="https://esgf-node.llnl.gov"
fetch_url=data_node+"/esg-search/wget?"
query_fmt = data_node+"/esg-search/search?sort=true&format=application%2Fsolr%2Bjson"
dict_dir="./dictionary"

vocab_url=query_fmt+"&limit=0&facets="

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Gets controlled vocabularly from ESGF and saves in JSON files",
    epilog=textwrap.dedent('''\
                           Vocabulary downloads can also be constrained by specified parameters
                           example: '''+sys.argv[0]+''' -r -t -ex -en -m -p cmip3'''))
parser.add_argument('-r', dest='realm', nargs='?', const=True, default=True)
parser.add_argument('-p', dest='project', nargs='?', const=True, default=True)
parser.add_argument('-prod', dest='product', nargs='?', const=True)
parser.add_argument('-m', dest='model', nargs='?', const=True, default=True)
parser.add_argument('-var', dest='variable', nargs='?', const=True)
parser.add_argument('-ver', dest='version', nargs='?', const=True)
parser.add_argument('-ex', dest='experiment', nargs='?', const=True, default=True)
parser.add_argument('-t', dest='time_frequency', nargs='?', const=True, default=True)
parser.add_argument('-i', dest='institute', nargs='?', const=True)
parser.add_argument('-en', dest='ensemble', nargs='?', const=True)
parser.add_argument('-in', dest='index_node', nargs='?', const=True)
parser.add_argument('-id', dest='id', nargs='?', const=True)
parser.add_argument('-c', dest='cmor_table', nargs='?', const=True)
args = parser.parse_args()
args_dict = vars(args)

# add args to facets for dictionaries
for key,value in args_dict.items():
    if (value == True): vocab_url=vocab_url+key+","

# specified constraints
for key,value in args_dict.items():
    if isinstance(value,str): vocab_url=vocab_url+"&"+key+"="+str(value)

# load json format of dictionaries
vocab = urllib.urlopen(vocab_url)
vocab = json.loads(vocab.read())["facet_counts"]["facet_fields"]

# save dictionary files
os.system("mkdir -p "+dict_dir)
for key,value in vocab.items():
    file = open(dict_dir+"/"+key+".json","w")
    val_list = re.sub(r'[0-9]+','',json.dumps(value).replace(",","").replace("[\"","").replace("]","").replace("\" ","")).split(" \"")
    file.write("{\n")
    file.write("\""+key+"\":{\n")
    for word in val_list[:-1]:
        file.write("\""+word+"\":"+"\""+word+"\",\n")
    file.write("\""+val_list[-1]+"\":"+"\""+val_list[-1]+"\"}")
    file.write("\n}")
    file.close()

