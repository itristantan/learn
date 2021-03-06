# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 23:01:08 2017

@author: tristan
"""

import requests
from bs4 import BeautifulSoup
import re
from common import parse_config,config_save
from pathlib import Path
import os

home = Path(os.path.expanduser("~"))
workdir=home/'.ss'
if not workdir.exists():
    workdir.mkdir()

FILENAME="ss2_{}_{}.json"

for file in workdir.glob("ss2*.json"):
    print("unlink {}".format(file))
    file.unlink()

def r1(pattern,text):
    m=re.search(pattern,text)
    if m:
        return m.group(1)

def r1_of(patterns,text):
    for p in patterns:
        x=r1(p,text)
        if x:
            return x

fake_headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

#感谢分享
url="http://www.ysguan.com/page/testss.html"

r=requests.get(url,headers=fake_headers)
soup=BeautifulSoup(r.text,"lxml")

div_all=soup.find_all("div",class_="testvpnitem")
for i,div in enumerate(div_all):
    config={}
    text=div.get_text().replace(u"：",":")
    try:
        config['server']=r1(u"服务器IP:(.*)",text).strip("\r")
        config['server_port']=int(r1(u"端口:(.*)",text).strip("\r"))
        config['password']=r1(u"密码:(.*)",text).strip("\r")
        config['method']=r1(u"加密方式:(.*)",text).strip("\r")
        config=parse_config(config)
        if config:
            print(config)
            filename=FILENAME.format(config['server'],config['server_port'])
            path_file=workdir/filename
            config_save(config,path_file)
    except Exception as e:
        print(e)
