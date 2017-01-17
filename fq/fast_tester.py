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
import platform
import shlex
import time
import os
import sys

home = Path(os.path.expanduser("~"))

win_app="sslocal"
url="http://www.google.co.jp"  #test url

DEBUG=0

plat=platform.system().lower()

def proxy_tester(config,url,num=10):

    assert num > 0
    global win_app

    local_port=int(config['local_port'])
    command_line="{app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port}"\
                " -t 300".format(app=win_app,
                              server=config['server'],
                              server_port=config['server_port'],
                              password=config['password'],
                              method=config['method'],
                              local_port=local_port)
    print("启动进程...")
    print(command_line)
    args=shlex.split(command_line)
    p=Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=False)
    print("pid: {}".format(p.pid))
    time.sleep(8)

    print("测试连接...")
    total_time=0.
    for i in range(num):
        total_time+=fetch_tester(url,PROXY='127.0.0.1',PROXYPORT=local_port,PROXYTYPE=7,VERBOSE=DEBUG)
        if total_time < 19999:
            break
        time.sleep(0.2)

    total_time=total_time/num
    print("{}次平均请求时间: {}".format(num,total_time))

    print("杀死进程，kill %s"%p.pid)
    if plat == 'windows':
        cmd="taskkill /f /t /pid {}".format(p.pid)
        print(getoutput(cmd))
    p.kill()
    return total_time

if __name__ == "__main__":

    config_file=home/'configs.json'
    configs=config_load(config_file)

    if not configs:
        print("没有加载到配置!")
        os.system("start \"fetch\" fetch.bat")
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

    config_result=[]
    for config,res in zip(configs,result):
        total_time=res.get()
        if total_time < 999:
            config['total_time']=total_time
            config_result.append(config)

    if len(config_result) == 0: sys.exit(1)
    configs=sorted(config_result,key=lambda k:k['total_time'])
    config_save(configs,config_file)

    print("*"*60)
    sortedkeys=['server','server_port','password','method','total_time']
    for cfg in configs:
        s=", ".join([str(cfg[k]) for k in sortedkeys if k in cfg.keys()])
        print(s)
