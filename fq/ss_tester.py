#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-13 14:15:14

@author: tanxin
"""

import os
import glob
import json
from subprocess import Popen,PIPE,getoutput
import shlex
import time
from io import BytesIO
import pycurl
from collections import OrderedDict

win_app="ss-local.exe"
url1="http://www.google.co.jp"
url2="http://www.python.org"
url=url1

results_d={}

def config_load(file):
    '''
    加载json配置
    '''
    try:
        with open(file,'r') as f:
            ret=json.load(f)
            return ret
    except Exception as e:
        raise e

def config_save(obj,file):
    '''
    保存json配置
    '''
    try:
        with open(file,'w') as fw:
            json.dump(obj,fw,indent=2)
    except Exception as e:
        raise e

def fetch_tester(url="http://www.baidu.com",param={}):
    '''
    代理服务器连通性测试
    代理地址端口: 127.0.0.1:1080 代理类型：socks5-hostname PROXYTYPE=7
    返回：成功，返回 响应时间，失败，返回 -1
    '''
    http_code=None
    buffer=BytesIO()
    c=pycurl.Curl()
    try:
        c.setopt(pycurl.URL,url)
        c.setopt(pycurl.CONNECTTIMEOUT, 10)
        c.setopt(pycurl.TIMEOUT, 30)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.MAXREDIRS, 5)
        c.setopt(pycurl.SSL_VERIFYPEER,0)
        c.setopt(pycurl.SSL_VERIFYHOST,0)
        c.setopt(pycurl.WRITEDATA,buffer)
        for k,v in param.items():
            c.setopt(vars(pycurl)[k],v)
        c.perform()
        http_code=c.getinfo(pycurl.RESPONSE_CODE)
        total_time=c.getinfo(pycurl.TOTAL_TIME)
        print("response code: {} ,total time: {}".format(http_code,total_time))
    except Exception as e:
        print(e)
    finally:
        c.close()
        if http_code == 200:
            return float(total_time)
        else:
            return -1

def proxy_tester(config):

    global results_d
    num=10

    payload=dict()
    payload['PROXY']='127.0.0.1'
    payload['PROXYTYPE']=7
    payload['PROXYPORT']=config['local_port']
    payload['VERBOSE']=0

    print("启动进程...")
    command_line="{app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port} -t 60".format(app=win_app,
            server=config['server'],
            server_port=config['server_port'],
            password=config['password'],
            method=config['method'],
            local_port=config['local_port'])
    print(command_line)
    args=shlex.split(command_line)
    proc=Popen(args,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=False)
    time.sleep(5)

    print("测试连接...")
    total_time=0
    result=[]
    for i in range(num):
        total_time=fetch_tester(url,param=payload)
        result.append(total_time)
        time.sleep(0.1)

    result.sort()
    total_time=sum(result[1:-1]) #去掉最高和最低
    print("{}次请求时间和: {}".format(num-2,total_time))
    k="{}:{}".format(config['server'],config['server_port'])
    results_d[k]=total_time

    print("杀死进程，kill %s"%proc.pid)
    command_line="taskkill /f /t /pid {}".format(proc.pid)
    ret=getoutput(command_line)
    print(ret)
    proc.kill()

if __name__ == "__main__":

    DEBUG=False
    configs=[]
    local_port=1080

    workdir=os.path.abspath(".")

    file_rule=os.path.join(workdir,"ss*.json")
    files=glob.glob(file_rule)
    for file in files:
        if DEBUG:
            print("加载配置: {}".format(file))
        config=config_load(file)
        configs.append(config)

    for config in configs:
        print(config['server'],config['server_port'],config['method'],config['password'],local_port)
        local_port+=1
        proxy_tester(config)

    # dictionary sorted by value
    results_d=OrderedDict(sorted(results_d.items(), key=lambda t: t[1]))
    print(results_d)
