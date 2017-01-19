#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2017-01-18 11:57:46

@author: tristan
"""

import multiprocessing as mp
import time

def foo_pool(x):
    time.sleep(1)
    return x*x

result_list = []
def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def apply_async_with_callback():
    pool = mp.Pool()
    for i in range(10):
        pool.apply_async(foo_pool, args = (i, ), callback = log_result)
    pool.close()
    pool.join()
    print(result_list)

if __name__ == '__main__':

    apply_async_with_callback()
