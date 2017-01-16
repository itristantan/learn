# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 11:20:31 2017

@author: tristan
"""

from common import config_save,get_config
from subprocess import getstatusoutput
import multiprocessing
from pathlib import Path
import platform
import sys
import time
import re
import os

home = Path(os.path.expanduser("~"))
workdir=home/'.ss'

plat=platform.system().lower()

if plat == 'windows':
    ping_shell="ping -n %s -w %s %s"
    ping_regex=re.compile(r"平均 = (\d+)ms")
else:
    ping_shell="ping -c %s -W %s %s"
    ping_regex=re.compile(r".*min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms")

def ping(host,count=3,timeout=1):
    global ping_regex,ping_shell
    cmd=ping_shell%(count,timeout,host)
    status,out=getstatusoutput(cmd)
    if status == 0:
        print("%s is alive."%host)
        match=ping_regex.search(out,re.IGNORECASE)
        if match:
            return float(match.group(1))
    print("%s is down."%host)
    return 9999.0

if __name__ == '__main__':

    start=time.time()

    configs=get_config(workdir) #加载配置，文件名规则："ss*.json"
    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    ip_list=list(set([config['server'] for config in configs if 'server' in config.keys()]))
    ping_result={}

    result=[]
    length=len(ip_list)
    process_number=length if length < 9 else 8
    pool = multiprocessing.Pool(processes=process_number)
    for host in ip_list:
        result.append(pool.apply_async(ping,(host,)))
    pool.close()
    pool.join()

    for host,res in zip(ip_list,result):
        ping=res.get()
        ping=float(ping) if ping else 9999.0
        print("host: {}, ping: {}ms".format(host,ping))
        ping_result[host]=ping

    for i in range(len(configs)):
        host=configs[i]['server']
        if host in ping_result.keys():
            configs[i]['ping_time']=ping_result[host]
        else:
            configs[i]['ping_time']=9999

    configs=sorted(configs,key=lambda k:k['ping_time'])
    config_save(configs,workdir/"configs.json")

    end=time.time()
    print("Run Time: {}".format(end-start))
