#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2017-01-14 12:03:11

@author: tristan
"""

def foo(*args, **kwargs):
    print("*"*50)
    print("type args:",type(args))
    print("type kwargs:",type(kwargs))
    print("args:",args)
    print("kwargs:",kwargs)

foo(1, 2, 3, 4)
foo(a=1, b=2, c=3)
foo(1,2,3,4, a=1, b=2, c=3)
foo('a', 1, None, a=1, b='2', c=3)
