# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 17:40:52 2017

@author: tristan
"""

from subprocess import getstatusoutput
from pathlib import Path
import os
import json
import socket

password="7be329"
method="aes-256-cfb"
param=" -H \"Content-Type: application/vnd.api+json\" -H \"Accept: application/vnd.api+json\" 2>nul"

home = Path(os.path.expanduser("~"))
workdir=home/'.ss'
if not workdir.exists():
    workdir.mkdir()

for file in workdir.glob("ssme*.json"):
    print("unlink {}".format(file))
    file.unlink()

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

def get_containers():
    ret=[]
    cmd="curl -n https://app.arukas.io/api/apps %s"%(param)
    status,out=getstatusoutput(cmd)
    if status == 0:
        try:
            dataobj=json.loads(out)
            for data in dataobj['data']:
                container_id=data['relationships']['container']['data']
                ret.append(container_id)
        except Exception as e:
            print(e)
    return ret

def get_port_mappings(container_id):
    ret=[]
    url="https://app.arukas.io/api/containers/%s"%container_id
    cmd="curl -n %s %s"%(url,param)
    status,out=getstatusoutput(cmd)
    if status == 0:
        obj=json.loads(out)
        port_mappings=obj['data']['attributes']['port_mappings']
        for port_mapping in port_mappings:
            if isinstance(port_mapping,list):
                ret.extend(port_mapping)
            else:
                ret.append(port_mapping)
    return ret

def main():
    cfg={}
    os.environ['home']=str(home)  #_netrc 文件存放位置 for windows
    containers=get_containers()
    for container in containers:
        container_id=container['id']
        print("*"*60)
        print(container_id)
        port_mapping=get_port_mappings(container_id)
        for port_map in port_mapping:
            container_port=port_map['container_port']
            server=socket.gethostbyname(port_map['host'])
            server_port=port_map['service_port']
            print(container_port,server,server_port)
            if container_port in [8388,8989]:
                cfg['server']=server
                cfg['server_port']=server_port
                cfg['password']=password
                cfg['method']=method
                filename="ssme_%s_%s.json"%(server,server_port)
                config_save(cfg,home/'.ss'/filename)

if __name__ == "__main__":

    main()
