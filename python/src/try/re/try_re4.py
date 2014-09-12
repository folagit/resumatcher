# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 23:58:46 2014

@author: dlmu__000
"""
import re
def test1():
    prog = re.compile("aaa")
    print  prog.match("aaa")
    
def test2():
    prog = re.compile("aaa")
    print  prog.match("baaa")
    
def test3():
    prog = re.compile("aaa")
    print  prog.match("aaab")
    
def test4():
    prog = re.compile("\baaa\b")
    print   prog.search("aaab")
    
def test5():
    prog = re.compile(r"\baaa\b")
    result =    prog.search("aaa")
    print result
    
def test6():
    prog = re.compile("aaa")
    result =   re.search(r'\baaa\b', 'aaa')
    print result
    
def test7(): 
    s = "aaa"
    c = r"\b"+s+r"\b"
    print c
    prog = re.compile(c)
    result =    prog.search("aaa")
    print result
    
test7()