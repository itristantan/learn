# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 23:01:08 2017

@author: tanxin
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import os

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

url="http://www.ysguan.com/page/testss.html"

r=requests.get(url,headers=fake_headers)
soup=BeautifulSoup(r.text,"lxml")

config={'server':'192.168.18.10',
      'server_port':8338,
      'password':'123456',
      'method':'aes-256-cfb',
      # 'local_address':'127.0.0.1',
      # 'local_port':1080,
      # 'fast_open':False,
      # 'timeout':300
      }

div_all=soup.find_all("div",class_="testvpnitem")
for i,div in enumerate(div_all):
    config.clear()
    text=div.get_text().replace(u"：",":")
    try:
        config['server']=r1(u"服务器IP:(.*)",text).strip("\r")
        config['server_port']=int(r1(u"端口:(.*)",text).strip("\r"))
        config['password']=r1(u"密码:(.*)",text).strip("\r")
        config['method']=r1(u"加密方式:(.*)",text).strip("\r")
        config_string=json.dumps(config,indent=2)

        file="shadowsocks{}.json".format(i+1)
        print("config write to file: {}".format(file))
        print(config_string)
        with open(file,'w') as fw:
            fw.write(config_string)
            fw.flush()
    except Exception as e:
        print(e)
