#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-14 15:05:22

@author: tanxin

多线程ping服务器，根据ping值排序，并保存配置

"""

import os
import glob
import json
import multiprocessing
import subprocess
import re
import time
import sys

workdir="config"

def config_load(file_path):
    '''
    加载json配置
    '''
    try:
        with open(file_path,'r',encoding="utf-8") as f:
            ret=json.load(f)
            return ret
    except Exception as e:
        print(e)

def config_save(objdata,file_path):
    '''
    保存json配置
    '''
    try:
        print("write to file: {}".format(file_path))
        with open(file_path,'w',encoding="utf-8") as fw:
            json.dump(objdata,fw,indent=2,ensure_ascii=False)
    except Exception as e:
        print(e)

def get_config(workdir="."):

    result=[]
    workdir=os.path.abspath(workdir)
    file_rule=os.path.join(workdir,"ss*.json")
    for file in glob.glob(file_rule):
        print("load file: {}".format(file))
        config=config_load(file)
        if config:
            result.append(config)
    return result

def ping_ip(ipaddr):
    pattern=re.compile(r"平均 = (\d+)ms")
    ping_cmd="ping -n 5 -w 1 %s"%ipaddr
    out=subprocess.getoutput(ping_cmd)
    match=pattern.search(out)
    if match:
        return float(match.group(1))

if __name__ == '__main__':

    start=time.time()

    workdir=os.path.abspath(workdir)
    os.chdir(workdir)
    configs=get_config(workdir) #加载配置，文件名规则："ss*.json"
    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    ip_list=list(set([config['server'] for config in configs if 'server' in config.keys()]))
    ping_result={}

    result=[]
    length=len(ip_list)
    process_number=length if length < 8 else 8
    pool = multiprocessing.Pool(processes=process_number)
    for ipaddr in ip_list:
        result.append(pool.apply_async(ping_ip,(ipaddr,)))
    pool.close()
    pool.join()

    for ipaddr,res in zip(ip_list,result):
        ping=res.get()
        ping=float(ping) if ping else 9999.0
        print("host: {}, ping: {}ms".format(ipaddr,ping))
        ping_result[ipaddr]=ping

    for i in range(len(configs)):
        host=configs[i]['server']
        if host in ping_result.keys():
            configs[i]['ping']=ping_result[host]
        else:
            configs[i]['ping']=9999

    configs=sorted(configs,key=lambda k:k['ping'])
    config_save(ping_result,"ping_result.txt")
    config_save(configs,"configs.txt")

    end=time.time()
    print("Run Time: {}".format(end-start))
