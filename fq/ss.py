#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-14 09:26:44

@author: tanxin
"""

from subprocess import Popen,PIPE,getoutput
import os
import time
import requests
import json
import sys
import glob
import re
import socket

workdir="config"
win_app="sslocal.exe"

def get_ipaddr(host_or_ip):
    if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',host_or_ip):
        return host_or_ip
    else:
        try:
            result=socket.getaddrinfo(host_or_ip,None)
            for res in result:
                return res[4][0]
        except Exception as e:
            pass

def ipinfo_region(host_or_ip):
    '''
    新浪ip信息api
    返回jsonobj ret=1
    '''
    region="unknow"
    ip=get_ipaddr(host_or_ip)
    if ip is None: return region
    try:
        url="http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip={}".format(ip)
        r=requests.get(url)
        if r.status_code == 200:
            r.encoding='utf-8'
            obj=r.json()
            if obj['ret'] == 1:
                region=obj['country']+' '+obj['province']
    except:
        pass
    return region

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

def run_app(win_app,config,log_file="shadowsocks.log"):
    #检查配置
    field=['server', 'server_port', 'method', 'password', 'local_port']
    for k in field:
        if k in config.keys() and config[k]:
            continue
        else:
            print("{} not in config.".format(k))
            return

    print("启动进程...")
    command_line="{app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port} "\
                "-t 300 -v 1> {log_file} 2>&1".format(app=win_app,
                                                      server=config['server'],
                                                      server_port=config['server_port'],
                                                      password=config['password'],
                                                      method=config['method'],
                                                      local_port=config['local_port'],
                                                      log_file=log_file)
    print(command_line)
    p=Popen(command_line,stdin=PIPE,shell=True)
    print("pid: {}".format(p.pid))
    time.sleep(5)
    p.terminate()
    p.kill()

if __name__ == '__main__':

    workdir=os.path.abspath(workdir)
    temp_path=os.getenv("TEMP")
    log_file=os.path.join(temp_path,"shadowsocks.log")
    config_file=os.path.join(workdir,"configs.txt")
    configs=config_load(config_file)
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
                                         cfg['ping']))

    config=configs[0]
    config['local_port']=1080
    print(getoutput("taskkill /f /t /im {}".format(win_app))) #清理进程
    run_app(win_app,config,log_file)

    if os.path.exists(log_file):
        print("打开日志文件:{}".format(log_file))
        with open(log_file,'r') as f:
            content=f.read()
            print(content)

    print("byebye!")
