#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-12 16:49:39

@author: tanxin

查找最快的shadowsocks服务器

"""

import multiprocessing
from subprocess import Popen,PIPE,getoutput
from io import BytesIO
import pycurl
import time
import os
import sys
from ss import config_load,config_save

workdir="config"
win_app="sslocal.exe"
url1="http://www.google.co.jp"
url2="http://www.python.org"
url=url1
DEBUG=0

def fetch_tester(url="http://www.baidu.com",**kwargs):
    '''
    代理服务器连通性测试
    代理地址端口: 127.0.0.1:1080 代理类型：socks5-hostname PROXYTYPE=7
    返回：成功，返回 响应时间，失败，返回 -1
    '''
    http_code=None
    buffer=BytesIO()
    c=pycurl.Curl()
    try:
        c.setopt(c.URL,url)
        c.setopt(c.CONNECTTIMEOUT, 8)
        c.setopt(c.TIMEOUT, 32)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.MAXREDIRS, 5)
        c.setopt(c.SSL_VERIFYPEER,0)
        c.setopt(c.SSL_VERIFYHOST,0)
        c.setopt(c.WRITEDATA,buffer)
        c.setopt(c.NOSIGNAL,1)
        #c.setopt(c.VERBOSE,1)
        for k,v in kwargs.items():
            c.setopt(vars(pycurl)[k],v)
        c.perform()
        http_code=c.getinfo(c.RESPONSE_CODE)
        total_time=c.getinfo(c.TOTAL_TIME)
        print("response code: {} ,total time: {}".format(http_code,total_time))
    except Exception as e:
        print(e)
    finally:
        c.close()
        if http_code == 200:
            return float(total_time)
        else:
            return -1

def proxy_tester(config,url="http://www.baidu.com",num=10):

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

def check_config(config):
    if isinstance(config,dict):
        field=['server', 'server_port', 'method', 'password']
        for k in field:
            if k in config.keys() and config[k]:
                continue
            else:
                return
        return True

if __name__ == "__main__":

    workdir=os.path.abspath(workdir)
    config_file=os.path.join(workdir,"configs.txt")
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
        config['total_time']=total_time if total_time > 0 else 9999.8
        config_result.append(config)

    configs=sorted(config_result,key=lambda k:k['total_time'])
    config_save(configs,config_file)
