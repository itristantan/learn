#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-16 10:52:15

@author: tristan
"""

import threading
import queue
import time

def worker(port):
    while 1:
        item = task_queue.get()
        if item is None:
            break
        threadname = threading.currentThread().getName()
        ident=threading.currentThread().ident
        item="#{},{},item={}---------127.0.0.1:{}".format(threadname,ident,item,port)
        done_queue.put(item)
        task_queue.task_done()
        time.sleep(0.01)

if __name__ == "__main__":

    num_worker_threads=4
    task_queue = queue.Queue()
    done_queue = queue.Queue()

    DEBUG=True
    configs=[]

    start_port=65501
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker,args=(start_port,))
        t.start()
        threads.append(t)
        start_port+=1

    configs=list(range(10))
    for config in configs:
        task_queue.put(config)

    task_queue.join()

    # stop workers
    for i in range(num_worker_threads):
        task_queue.put(None)

    print('*'*60)
    result=[]
    while not done_queue.empty():
        result.append(done_queue.get())

    for res in result:
        print(res)
