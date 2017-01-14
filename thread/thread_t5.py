#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-13 21:16:05

@author: tanxin
"""

import time
import random
import threading
import queue

def worker():
    while True:
        item = task_queue.get()
        if item is None:
            break
        do_work(item)
        task_queue.task_done()

def do_work(item):
    ret=int(item)*2
    done_queue.put(ret)

def source():
    return list(range(10))

num_worker_threads=4

task_queue = queue.Queue()
done_queue = queue.Queue()

threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in source():
    task_queue.put(item)

# block until all tasks are done
task_queue.join()

# stop workers
for i in range(num_worker_threads):
    task_queue.put(None)

result=[]
while not done_queue.empty():
    result.append(done_queue.get())

print(result)
