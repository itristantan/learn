#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-13 14:15:14

@author: tristan
"""

from subprocess import Popen,PIPE,getoutput
from common import config_load,config_save,fetch_tester
from pathlib import Path
import threading
import platform
import shlex
import queue
import time
import os
import sys

home = Path(os.path.expanduser("~"))

app="sslocal"
url="http://www.google.co.jp"
DEBUG=0

plat=platform.system().lower()

def proxy_tester(config,url,num=10):

    assert num > 0
    global app

    local_port=int(config['local_port'])
    command_line="{app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port}"\
                " -t 300".format(app=app,
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
    time.sleep(10)

    print("测试连接...")
    total_time=0.
    for i in range(num):
        total_time+=fetch_tester(url,PROXY='127.0.0.1',PROXYPORT=local_port,PROXYTYPE=7,VERBOSE=DEBUG)
        if total_time > 19999:
            break
        time.sleep(0.2)

    total_time=total_time/num
    print("{}次平均请求时间: {}".format(num,total_time))

    print("杀死进程，kill {}".format(p.pid))
    if plat == 'windows':
        cmd="taskkill /f /t /pid {}".format(p.pid)
        print(getoutput(cmd))
    p.kill()
    return total_time

def worker(url,port):
    while 1:
        item = task_queue.get()
        if item is None:
            break
        item['local_port']=port
        total_time=proxy_tester(item,url)
        item['total_time']=total_time if total_time >0 else 9999.3
        done_queue.put(item)
        task_queue.task_done()

if __name__ == "__main__":

    config_file=home/'configs.json'
    configs=config_load(config_file)

    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    result=[]
    length=len(configs)
    num_worker_threads=length if length < 9 else 9

    task_queue = queue.Queue()
    done_queue = queue.Queue()

    threads = []
    port=1081
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker,args=(url,port))
        t.start()
        threads.append(t)
        port+=1

    for item in configs:
        task_queue.put(item)

    # block until all tasks are done
    task_queue.join()

    # stop workers
    for i in range(num_worker_threads):
        task_queue.put(None)

    configs=[]
    while not done_queue.empty():
        cfg=done_queue.get()
        if cfg['total_time'] < 999:
            configs.append(cfg)

    if len(configs) == 0: sys.exit(1)
    configs=sorted(configs,key=lambda k:k['total_time']) #排序
    config_save(configs,config_file) #保存
    # config=configs[0]
    # config['local_port']=1080
    # config_save(config,home/'shadowsocks.json')

    print("*"*60)
    sortedkeys=['server','server_port','password','method','ping_time','total_time']
    for cfg in configs:
        s=", ".join([str(cfg[k]) for k in sortedkeys if k in cfg.keys()])
        print(s)
