#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-13 16:58:57

@author: tanxin
"""

import os

import threading

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print("I am %s" % (self.name))

if __name__ == "__main__":

    for i in range(0, 10):
        my_thread = MyThread()
        my_thread.start()
        my_thread.join()
