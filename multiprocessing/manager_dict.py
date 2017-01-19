#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-18 10:14:35

@author: tristan
"""

#multiprocessing_manager_dict.py
import multiprocessing
import pprint


def worker(d, key, value):
    d[key] = value


if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    d = mgr.dict()
    jobs = [
        multiprocessing.Process(
            target=worker,
            args=(d, i, i * 2),
        )
        for i in range(10)
    ]
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()
    print('Results:', d)
