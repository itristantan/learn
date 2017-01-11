# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 17:39:24 2017

@author: tanxin
"""

import json
import glob
import os

def load_config(filename):
    try:
        with open(filename,'r') as f:        
            return json.load(f)
    except Exception as e:
        print(e)
        
def save_config(obj,filename):
    with open(filename,'w') as fw:
        json.dump(obj,fw,indent=2)        

gui_configfile=r"e:\fq\bin\gui-config.json"
print(gui_configfile)

gui_config=load_config(gui_configfile)
configs=gui_config['configs']
    
path_rule=r"e:\fq\shadowsocks*.json"
files=glob.iglob(path_rule)
for file in files:        
    print(file)
    config=load_config(file)
    if config:
        if config not in configs:
            configs.append(config)
            
gui_config['configs']=configs 

save_config(gui_config,gui_configfile) 
print(gui_config)          
        
