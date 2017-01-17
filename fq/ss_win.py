#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-14 09:26:44

@author: tristan
"""

from subprocess import Popen,PIPE,getoutput
from common import config_load,config_save
from pathlib import Path
import sys
import os
import time

home = Path(os.path.expanduser("~"))
win_app="sslocal"

if __name__ == '__main__':

    configs=config_load(home/"configs.json")

    if not configs:
        print("没有加载到配置!")
        sys.exit(1)

    config=configs[0]
    config['local_port']=1080
    print(getoutput("taskkill /f /t /im {}".format(win_app))) #清理进程

    print("启动进程...")
    command_line="start /MIN \"fuckgfw\" {win_app} -s {server} -p {server_port} -k {password} -m {method} -l {local_port} "\
            "-t 300 -v".format(win_app=win_app,
                              server=config['server'],
                              server_port=config['server_port'],
                              password=config['password'],
                              method=config['method'],
                              local_port=config['local_port'])
    print(command_line)
    p=Popen(command_line,stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    poll=p.poll()
    while poll is None:
        time.sleep(1)
        poll=p.poll()
        print("poll is %s."%poll)
    p.kill()

    print("byebye!")
