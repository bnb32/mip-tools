import sys,subprocess,os
import json
import numpy as np
import textwrap
import pexpect
import multiprocessing

try:
    import urllib.request as urllib
except ImportError:
    import urllib

def run_query(args,args_dict,query_url):

    if args.query:
    
        # printed fields in query
        for key,value in args_dict.items():
            if ( key != 'query' and key != 'data_dir' ):
                if(value == True or isinstance(value,str)): 
                    query_url+='%s,' %(key)
    
        # specified fields in query
        for key,value in args_dict.items():
            if ( key != 'query' and key != 'data_dir'):
                if isinstance(value,str): 
                    query_url+='&%s=%s' %(key,str(value))
        
        # read query result
        response = urllib.urlopen(query_url)
        response = json.loads(response.read())
        
        if (len(response['response']['docs']) == 0): 
            print('no query results'); exit()
          
        # print query result
        print('\n %s results found' %(json.dumps(response['response']['numFound'])))
        print('Showing results %s through %s \n' %(str(args.offset),str(args.offset+args.limit-1)))
        for i in range(len(response['response']['docs'])):
            mylist = []; variables = ''
            for key,value in response['response']['docs'][i].items():
                entry='%s=%s' %(json.dumps(key),json.dumps(value))
                if ((str(key) != 'score') and (str(key) != 'variable')): 
                    mylist.append(entry.replace('\"','').replace(']','').replace('[',''))
                if (str(key) == 'variable'): 
                    variables+=entry
            if (variables != ''): 
                mylist.append(variables.replace('\"','').replace(']','').replace('[',''))    
            print('[%s] \n' % ', '.join(map(str, mylist)))
        exit()    

def setup_wget_script(args,args_dict,fetch_url,script_name):

    for key,value in args_dict.items():
        if ( key != 'query' and key != 'data_dir'):
            if isinstance(value,str):
                if (key=='id'): key='dataset_id'
                script_name+='_%s' %(str(value.split('|')[0]))
                fetch_url+='&%s=%s'%(key,str(value))
    
    
    script_name+='.sh'    
    
    if args_dict['limit']: 
        fetch_url+='&limit=%s' %(str(args_dict['limit']))
    if args_dict['offset']: 
        fetch_url+='&offset=%s'%(str(args_dict['offset']))
    
    return [fetch_url,script_name]


def get_wget_script(args,args_dict,dictionaries,query_url,fetch_url,script_name,data_dir):    

    # check dictionaries for valid entries
    
    for key,value in args_dict.items():
        if ( key in dictionaries.keys() ):
            if isinstance(value,str):
                dict_name = dictionaries[key]
                if value not in dict_name:
                    print('invalid %s entry' %(key)); 
                    exit()
    
    
    run_query(args,args_dict,query_url)

    # setup download script

    [fetch_url,script_name]=setup_wget_script(args,args_dict,fetch_url,script_name)
    
    # get download script
    
    fetch_cmd = 'wget -O %s %s' %(script_name,fetch_url)
    process = subprocess.Popen(fetch_cmd.split(), stdout=subprocess.PIPE)
    output,error = process.communicate()
    
    # check for empty script
    
    if 'bash' not in open(script_name,'r').readline():
        print('Empty script downloaded: This is an invalid parameter set')
        rm_cmd = 'rm -f ./%s' %(script_name)
        subprocess.Popen(rm_cmd.split(), stdout=subprocess.PIPE)
        exit()
    
    # make data dir for download
    
    mkdir_cmd = 'mkdir -p %s' %(data_dir)
    mv_cmd = 'mv %s %s' %(script_name,data_dir)
    os.system(mkdir_cmd+'; '+mv_cmd)

    return script_name

def run_wget_script(data_dir,script_name,openid,password):
    os.chdir(data_dir)
    dl_cmd = 'bash %s/%s -H' %(data_dir,script_name)
    child = pexpect.spawn(dl_cmd)
    child.expect('Enter your openid :')
    child.sendline(openid)
    child.expect('Enter password :')
    child.sendline(password)
    child.interact()

def par_run(function,*args):
    thread=multiprocessing.Process(target=function,args=(args))
    thread.start()
