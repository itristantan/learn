#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-13 14:15:14

@author: tristan
"""

import multiprocessing
from subprocess import Popen,PIPE,getoutput
from common import config_load,config_save,fetch_tester
from pathlib import Path
import time
import os
import sys

workdir=Path.cwd()
win_app="sslocal"
# url="http://www.python.org"
url="http://www.google.co.jp"
DEBUG=0

def proxy_tester(config,url,num=10):

    assert num > 0
    global win_app

    local_port=int(config['local_port'])
    command_line="{app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port}"\
                " -t 60".format(app=win_app,
                              server=config['server'],
                              server_port=config['server_port'],
                              password=config['password'],
                              method=config['method'],
                              local_port=local_port)
    print("启动进程...")
    print(command_line)
    p=Popen(command_line,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    print("pid: {}".format(p.pid))
    time.sleep(3)

    print("测试连接...")
    total_time=0.
    for i in range(num):
        total_time+=fetch_tester(url,PROXY='127.0.0.1',PROXYPORT=local_port,PROXYTYPE=7,VERBOSE=DEBUG)
        if total_time < -3:
            break
        time.sleep(0.2)

    total_time=total_time/num
    print("{}次平均请求时间: {}".format(num,total_time))

    print("杀死进程，kill %s"%p.pid)
    command_line="taskkill /f /t /pid {}".format(p.pid)
    ret=getoutput(command_line)
    print(ret)
    return total_time

if __name__ == "__main__":

    config_file=workdir/'configs.txt'
    configs=config_load(config_file)
    config_result=[]

    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    result=[]
    length=len(configs)
    process_number=length if length < 9 else 8
    pool = multiprocessing.Pool(processes=process_number)
    local_port=1081
    for config in configs:
        config['local_port']=local_port
        result.append(pool.apply_async(proxy_tester,(config,url)))
        local_port+=1
    pool.close()
    pool.join()

    for config,res in zip(configs,result):
        total_time=res.get()
        print("host:{}, port: {}, total time:{}".format(config['server'],config['server_port'],total_time))
        if total_time > 0:
            config['total_time']=total_time
            config_result.append(config)

    configs=sorted(config_result,key=lambda k:k['total_time'])
    config_save(configs,config_file)
