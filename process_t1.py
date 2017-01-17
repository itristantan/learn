#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-16 16:34:34

@author: tristan
"""

import multiprocessing
import time
import os

def func(msg):
    pid=os.getpid()
    ppid=os.getppid()
    time.sleep(0.1)
    return "ppid={},pid={},msg={}".format(ppid,pid,msg)

if __name__ == "__main__":

    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in range(10):
        msg = "hello %d" %(i)
        result.append(pool.apply_async(func, (msg, )))

    pool.close()
    pool.join()

    for res in result:
        print(res.get())

    print("Sub-process(es) done.")
