# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 17:50:11 2014

@author: dlmu__000
"""

a = [i for i in range(1,5)]
print a 

b = [ ('b', i , "ff" ) for i in range(1,5)]
print b 

c = [ ['b', i , "ff" ] for i in range(1,5)]
print c 

d = [ {'d': i } for i in range(1,5)]
print d 

e = [ {'id': i , "val" : i*10 } for i in range(1,5)]
print e 