#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-18 10:16:20

@author: tristan
"""

#multiprocessing_pool.py
import multiprocessing
import time

def do_calculation(data):
    return data * 2


def start_process():
    time.sleep(0.2)
    print('Starting', multiprocessing.current_process().name)

if __name__ == '__main__':
    inputs = list(range(10))
    print('Input   :', inputs)

    builtin_outputs = map(do_calculation, inputs)
    print('Built-in:', builtin_outputs)

    pool_size = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(
        processes=pool_size,
        initializer=start_process,
    )
    pool_outputs = pool.map(do_calculation, inputs)
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print('Pool    :', pool_outputs)
