#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-14 09:26:44

@author: tristan
"""

from subprocess import Popen,PIPE,getoutput
from common import config_load,config_save
from pathlib import Path
import time
import requests
import sys
import re
import socket
import os

home = Path(os.path.expanduser("~"))
workdir=home/'.ss'
if not workdir.exists():
    workdir.mkdir()

win_app="sslocal"

socket.setdefaulttimeout(3)
g_ipcheck = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')

def checkipvalid(ip):
    """检查ipv4地址的合法性"""
    ret = g_ipcheck.match(ip)
    if ret is not None:
        "each item range: [0,255]"
        for item in ret.groups():
            if int(item) > 255:
                return 0
        return 1
    else:
        return 0

def ipinfo_region(ip):
    '''
    新浪ip信息api
    返回jsonobj ret=1
    '''
    region="unknow"
    try:
        if checkipvalid(ip) == 0:
            ip=socket.gethostbyname(ip) #获取真实ip地址
        url="http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip={}".format(ip)
        r=requests.get(url)
        if r.status_code == 200:
            r.encoding='utf-8'
            obj=r.json()
            if obj['ret'] == 1:
                region=obj['country']+' '+obj['province']
    except Exception as e:
        print(e)
    return region

def run_winapp(win_app,config):

    print("启动进程...")
    command_line="start /MIN \"fuckgfw\" {app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port} "\
            "-t 300 -v".format(app=win_app,
                              server=config['server'],
                              server_port=config['server_port'],
                              password=config['password'],
                              method=config['method'],
                              local_port=config['local_port'])
    print(command_line)
    p=Popen(command_line,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    poll=p.poll()
    while poll is None:
        time.sleep(1)
        poll=p.poll()
        print("poll is %s."%poll)
    p.kill()

if __name__ == '__main__':

    configs=config_load(workdir/"configs.json")
    region_result={}

    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    for cfg in configs:
        host=cfg['server']
        if host not in region_result.keys():
            region_result[host]=ipinfo_region(cfg['server'])
        region=region_result[host]
        region_result[host]=ipinfo_region(cfg['server'])
        print("{0} {1} {2} {3} {4} {5}".format(cfg['server'],
                                         cfg['server_port'],
                                         cfg['password'],
                                         cfg['method'],
                                         region,
                                         cfg['ping_time']))

    config=configs[0]
    config['local_port']=1080
    config_save(config,home/'shadowsocks.json')

    print(getoutput("taskkill /f /t /im {}".format(win_app))) #清理进程

    run_winapp(win_app,config) #for windows

    print("byebye!")
