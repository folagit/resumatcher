# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 18:14:41 2014

@author: dlmu__000
"""
g = lambda x: x**3
 
print g(3)

def useLamda(num, lam):
    return lam(num)
    
print useLamda(2,g)
print useLamda(2,lambda x: x*10)