# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 22:26:26 2014

@author: dlmu__000
"""

def foo(arg): 
    x = 1
    print locals()
    

foo(10)
foo(True)

print locals()
print 
print
print globals()