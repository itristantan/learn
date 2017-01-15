#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-13 20:37:10

@author: tristan
"""

import threading
import time

class Test:

    cache = {}

    @classmethod
    def get_value(self, key):
        value = Test.cache.get(key, [])
        return len(value)

    @classmethod
    def store_value(self, key, value):
        if key not in Test.cache:
            Test.cache[key] = list(range(value))
        else:
            Test.cache[key].extend(list(range(value)))
        return len(Test.cache[key])

    @classmethod
    def release_value(self, key):
        if key in Test.cache:
            Test.cache.pop(key)
        return True

    @classmethod
    def print_cache(self):
        print('print_cache:')
        for key in Test.cache:
            print('key: %d, value:%d' % (key, len(Test.cache[key])))

def worker(number, value):
    key = number % 5
    print('threading: %d, store_value: %d' % (number, Test.store_value(key, value)))
    time.sleep(0.5)
    print('threading: %d, release_value: %s' % (number, Test.release_value(key)))

if __name__ == '__main__':
    thread_num = 3

    thread_pool = []
    for i in range(thread_num):
        th = threading.Thread(target=worker,args=[i, 1000000])
        thread_pool.append(th)
        thread_pool[i].start()

    for thread in thread_pool:
        threading.Thread.join(thread)

    Test.print_cache()
    time.sleep(1)

    thread_pool = []
    for i in range(thread_num):
        th = threading.Thread(target=worker,args=[i, 100000])
        thread_pool.append(th)
        thread_pool[i].start()

    for thread in thread_pool:
        threading.Thread.join(thread)

    Test.print_cache()
    time.sleep(1)
