#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-01-04 01:58:36
# @Author  : tanxin (i_tristan@163.com)
# @Link    :
# @Version : $Id$

import os,sys
import requests
import json
from collections import OrderedDict
url="https://superfreess.arukascloud.io/2ac56b41-0592-403e-9948-25faef4bc124"

workdir="config"
workdir=os.path.abspath(workdir)

dataobj=None
r=requests.get(url)
if r.status_code==200:
    try:
        dataobj=r.json()
    except Exception as e:
        print(e)
if dataobj is None:
    print("没有获取到配置。")
    sys.exit()

sortedvalue='server,server_port,local_address,local_port,password,timeout,method,fast_open'.split(',')

for i,item in enumerate(dataobj):
    appid=item.pop('appid')
    print(item)
    obj=OrderedDict(sorted(item.items(), key=lambda d:sortedvalue.index(d[0])))
    s=json.dumps(obj,indent=2)
    print(s)

    filename="ss_{}_{}.json".format(obj['server'],obj['server_port'])
    filename=os.path.join(workdir,filename)
    with open(filename,'w') as fw:
        fw.write(s)
        fw.flush()
