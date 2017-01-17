# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 11:20:31 2017

@author: tristan
"""

from io import BytesIO
import pycurl
import json

def config_load(path_file):
    '''
    加载json配置
    '''
    try:
        with path_file.open('r',encoding='utf-8') as f:
            ret=json.load(f)
            return ret
    except Exception as e:
        print(e)

def config_save(objdata,path_file):
    '''
    保存json配置
    '''
    try:
        print("write to file: {}".format(path_file))
        with path_file.open('w',encoding='utf-8') as fw:
            json.dump(objdata,fw,indent=2,ensure_ascii=False)
    except Exception as e:
        print(e)

def get_config(workdir):
    result=[]
    for path_file in workdir.glob("ss*.json"):
        print("load file: {}".format(path_file))
        config=config_load(path_file)
        if config:
            result.append(config)
    return result

def parse_config(item):
    config={}
    fields=['server', 'server_port', 'password', 'method', 'fast_open']
    for k in fields:
        if k in item.keys():
            config[k]=item[k]
        else:
            config[k]=None
    if config['fast_open'] is None:
        config.pop('fast_open')
    if all(config.values()):
        return config

def fetch_tester(url,**kwargs):
    '''
    代理服务器连通性测试 PROXY='127.0.0.1' PROXYPORT=1080 PROXYTYPE=7
    代理地址端口: 127.0.0.1:1080 代理类型：socks5-hostname
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
            return 9999.1
