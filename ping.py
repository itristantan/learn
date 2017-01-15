# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 11:20:31 2017

@author: tristan
"""

from subprocess import getstatusoutput
import re
import platform

plat=platform.system().lower()

if plat == 'windows':
    ping_shell="ping -n %s -w %s %s"
    ping_regex=re.compile(r"平均 = (\d+)ms")
else:
    ping_shell="ping -c %s -W %s %s"
    ping_regex=re.compile(r".*min/avg/max/mdev = ([\d\.]+)/([\d\.]+)/([\d\.]+)/([\d\.]+) ms")

def ping(host,count=3,timeout=1):
    global ping_regex,ping_shell
    cmd=ping_shell%(count,timeout,host)
    status,out=getstatusoutput(cmd)
    if status == 0:
        print("%s is alive."%host)
        match=ping_regex.search(out,re.IGNORECASE)
        if match:
            return float(match.group(1))
    print("%s is down."%host)
    return 9999.0


host="www.baidu.com"
time=ping(host,3)

print(time)


