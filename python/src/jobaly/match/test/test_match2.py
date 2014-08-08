# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 00:56:56 2014

@author: dlmu__000
"""
import sys
sys.path.append("..") 
import unittest
from matcher  import *

tokens1 = ["aaa","bbb","ccc","ddd"]

def test_seq1():
    
    matcher1 = TokenMatcher("aaa") 
    matcher2 = TokenMatcher(["bbb","ccc"]) 
    seq1 = SeqMatcher([matcher1,matcher2])
   
    print seq1(tokens1)
    
    
    
test_seq1()