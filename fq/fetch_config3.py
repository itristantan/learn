# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 18:00:33 2017

@author: tristan
"""

from common import config_save,parse_config
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import re

workdir=Path('config')
FILENAME="ss3_{}_{}.json"

for file in workdir.glob("ss3*.json"):
    file.unlink()

def r1(pattern,text):
    m=re.search(pattern,text)
    if m:
        return m.group(1)

url="https://freevpnss.cc/#shadowsocks"

r=requests.get(url)
r.encoding='utf-8'
soup=BeautifulSoup(r.text,'lxml')

div_all=soup.find_all(class_="panel-body")
for item in div_all:
    text=item.get_text()
    config={}
    config['server']=r1("服务器地址：(.*)",text)
    config['server_port']=r1("端口：(.*)",text)
    config['password']=r1("密.*码：(.*)",text)
    config['method']=r1("加密方式：(.*)",text)
    config=parse_config(config)
    if config:
        print(config)
        filename=FILENAME.format(config['server'],config['server_port'])
        path_file=workdir/filename
        config_save(config,path_file)
