#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-12 16:49:39

@author: tristan
"""

from subprocess import Popen,PIPE,getoutput
from collections import OrderedDict
import threading
import queue
from io import BytesIO
import shlex
import pycurl
import glob
import json
import time
import os

payload=dict()
payload['PROXY']='127.0.0.1'
payload['PROXYTYPE']=7
payload['VERBOSE']=0

win_app="ss-local.exe"
url1="http://www.google.co.jp"
url2="http://www.python.org"
url=url1

def config_load(file_path):
    '''
    加载json配置
    '''
    try:
        if DEBUG:
            print("read file: {}".format(file_path))
        with open(file_path,'r') as f:
            ret=json.load(f)
            return ret
    except Exception as e:
        print(e)

def config_save(objdata,file_path):
    '''
    保存json配置
    '''
    try:
        if DEBUG:
            print("write to file: {}".format(file_path))
        with open(file_path,'w') as fw:
            json.dump(objdata,fw,indent=2)
    except Exception as e:
        print(e)

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
        c.setopt(c.URL,url)
        c.setopt(c.CONNECTTIMEOUT, 10)
        c.setopt(c.TIMEOUT, 30)
        c.setopt(c.FOLLOWLOCATION, 1)
        c.setopt(c.MAXREDIRS, 5)
        c.setopt(c.SSL_VERIFYPEER,0)
        c.setopt(c.SSL_VERIFYHOST,0)
        c.setopt(c.WRITEDATA,buffer)
        c.setopt(c.NOSIGNAL,1)
        for k,v in param.items():
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

def proxy_tester(config,num=10):

    global payload

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
    payload['PROXYPORT']=config['local_port']
    total_time=0
    result=[]
    for i in range(num):
        total_time=fetch_tester(url,param=payload)
        result.append(total_time)
        time.sleep(0.1)

    result.sort()
    total_time=sum(result[1:-1]) #去掉最高和最低
    print("{}次请求时间和: {}".format(num-2,total_time))

    print("杀死进程，kill %s"%proc.pid)
    command_line="taskkill /f /t /pid {}".format(proc.pid)
    ret=getoutput(command_line)
    print(ret)
    # proc.kill()
    return total_time

def load_config_all(workdir='.'):

    configs=[]
    file_rule=os.path.join(workdir,"ss*.json")
    files=glob.glob(file_rule)
    for file in files:
        config=config_load(file)
        if not config:
            continue
        if all((config['server'],config['server_port'],config['password'],config['method'])):
            configs.append(config)
    return configs

def worker():
    while True:
        item = task_queue.get()
        if item is None:
            break
        do_work(item)
        task_queue.task_done()

def do_work(config):
    print ('thread %s is running...' % threading.current_thread().name)
    ret=proxy_tester(config)
    config['total_time']=ret
    done_queue.put(config)

if __name__ == "__main__":

    num_worker_threads=4
    task_queue = queue.Queue()
    done_queue = queue.Queue()

    DEBUG=True
    configs=[]
    local_port=1080

    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    workdir=os.path.abspath(".")
    configs=load_config_all(workdir)

    for config in configs:
        local_port+=1
        print(config['server'],config['server_port'],config['method'],config['password'],local_port)
        config['local_port']=local_port
        task_queue.put(config)

    # dictionary sorted by value
    # results_d=OrderedDict(sorted(results_d.items(), key=lambda t: t[1]))
    # print(results_d)
    # block until all tasks are done
    task_queue.join()

    # stop workers
    for i in range(num_worker_threads):
        task_queue.put(None)

    print('*'*60)
    result=[]
    while not done_queue.empty():
        result.append(done_queue.get())

    for d in result:
        print(d['server'],d['server_port'],d['total_time'])

