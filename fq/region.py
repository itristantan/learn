#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-17 14:09:38

@author: tristan
"""

from common import config_load,config_save
from pathlib import Path
import time
import requests
import sys
import re
import socket
import os

home = Path(os.path.expanduser("~"))

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

if __name__ == '__main__':

    configs=config_load(home/"configs.json")
    region_result=config_load(home/"region.json")
    if region_result is None: region_result={}
    region_length=len(region_result)

    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    print("*"*60)
    sortedkeys=['server','server_port','password','method','region','ping_time','total_time']
    for cfg in configs:
        host=cfg['server']
        if host not in region_result.keys():
            region_result[host]=ipinfo_region(cfg['server'])
        region=region_result[host]
        cfg['region']=region
        s=", ".join([str(cfg[k]) for k in sortedkeys if k in cfg.keys()])
        print(s)

    cfg=configs[0]
    cfg['local_port']=1080
    if 'ping_time' in cfg.keys(): cfg.pop('ping_time')
    if 'total_time' in cfg.keys(): cfg.pop('total_time')
    if 'region' in cfg.keys(): cfg.pop('region')
    config_save(cfg,home/'shadowsocks.json')

    if len(region_result) != region_length:
        config_save(region_result,home/'region.json')

    print("*"*60)
    print("byebye!")
