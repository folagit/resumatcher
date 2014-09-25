# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 23:17:42 2014

@author: dlmu__000
"""

import inspect
import os
import sys

def get_my_path():
    try:
        filename = __file__ # where we were when the module was loaded
    except NameError: # fallback
        filename = inspect.getsourcefile(get_my_path)
    return os.path.realpath(filename)

# path to ConfigManager.py
cm_path = get_my_path()
print "cm_path=" , cm_path
# go 6 directory levels up
sp_path = reduce(lambda x, f: f(x), [os.path.dirname]*6, cm_path)

print "sp_path=" , sp_path