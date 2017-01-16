#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-15 20:01:07

@author: tanxin
"""

from threading import Thread
import subprocess
from Queue import Queue

num_threads=3
ips=['127.0.0.1','116.56.148.187']
q=Queue()
def pingme(i,queue):
    while True:
        ip=queue.get()
        print 'Thread %s pinging %s' %(i,ip)
        ret=subprocess.call('ping -c 1 %s' % ip,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)
        if ret==0:
            print '%s is alive!' %ip
        elif ret==1:
            print '%s is down...'%ip
        queue.task_done()

#start num_threads threads
for i in range(num_threads):
    t=Thread(target=pingme,args=(i,q))
    t.setDaemon(True)
    t.start()

for ip in ips:
    q.put(ip)
print 'main thread waiting...'
q.join();print 'Done'
