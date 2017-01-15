#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 01:58:36
# @Author  : tanxin (i_tristan@163.com)
# @Link    :
# @Version : $Id$

import requests
from common import config_save,parse_config
from pathlib import Path

url="https://superfreess.arukascloud.io/2ac56b41-0592-403e-9948-25faef4bc124"

workdir=Path('config')
FILENAME="ss1_{}_{}.json"

for file in workdir.glob("ss1*.json"):
    file.unlink()

obj=None
r=requests.get(url)
if r.status_code==200:
    try:
        obj=r.json()
    except Exception as e:
        print(e)
if obj is None:
    print("没有获取到配置。")
    sys.exit()

if isinstance(obj,list):
    for item in obj:
        config=parse_config(item)
        if config:
            print(config)
            filename=FILENAME.format(item['server'],item['server_port'])
            path_file=workdir/filename
            config_save(config,path_file)
