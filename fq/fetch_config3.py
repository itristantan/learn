# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:00:33 2017

@author: tanxin
"""

import requests
from bs4 import BeautifulSoup
import subprocess
import re
import os
import time
import json

workdir="config"
workdir=os.path.abspath(workdir)

def r1(pattern,text):
    m=re.search(pattern,text)
    if m:
        return m.group(1)

url="https://freevpnss.cc/#shadowsocks"

r=requests.get(url)
r.encoding='utf-8'
#print(r.text)
soup=BeautifulSoup(r.text,'lxml')

local_port=1081
returns={}

div_all=soup.find_all(class_="panel-body")
for item in div_all:
    text=item.get_text()
    config={}
    config['server']=r1("服务器地址：(.*)",text)
    config['server_port']=r1("端口：(.*)",text)
    config['password']=r1("密.*码：(.*)",text)
    config['method']=r1("加密方式：(.*)",text)
    if all(config.values()):
        file="ss_{}_{}.json".format(config['server'],config['server_port'])
        file=os.path.join(workdir,file)
        print("config save to file: {}".format(file))
        config_string=json.dumps(config,indent=2)
        with open(file,"w") as fw:
            fw.write(config_string)
            fw.flush()
