# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 09:32:56 2017

@author: tristan
"""

import os,sys

os.system("set PYTHONIOENCODING=utf-8")
# os.environ["PYTHONIOENCODING"]="utf-8"

print(sys.stdin.encoding)
print(sys.stdout.encoding)
print(sys.stderr.encoding)

mystr="我是中文字体"

code = sys.getfilesystemencoding()

print(code)
sys.stdout.write(mystr)
