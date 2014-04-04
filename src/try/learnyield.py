# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 23:40:22 2014

@author: dlmu__000
"""

def h():
    print 'Wen Chuan'
    yield 5
    print 'Fighting!'

c = h()
c.next()
c.next()