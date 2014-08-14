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
  
def test_output():  
      class OutTokenMatcher(TokenMatcher):
           def __init__(self, tokens, catchfun=lambda x:x , outfun=lambda x: x):
               TokenMatcher.__init__(self,tokens, catchfun, outfun)
               
      matcher1 = OutTokenMatcher(["aaa"])
      matcher2 = OutTokenMatcher(["bbb", "ccc"])
      matcher1.findMatching(tokens1)
      alt1 = AlternateMatcher([matcher1,matcher2])  
      
      print alt1.findMatching(tokens1)  
      print alt1.catchMacher
      print alt1.catchMacher.output()
      print alt1.output()
      
def test_oper1():
     matcher1 = BaseMatcher() 
     matcher2 = BaseMatcher() 
     
     matcher3 = matcher1 + matcher2   
    
     matcher1 = TokenMatcher("aaa") 
     matcher2 = TokenMatcher("bbb") 
     
     matcher3 = matcher1 + matcher2

def createInstance(token, clazz):
     return     clazz(token) 
     
def testCreateClass():
    matcher1 = createInstance("aaa", TokenMatcher)
    print type(matcher1)
    print isinstance(matcher1,TokenMatcher )
    print matcher1(tokens1)
         
testCreateClass()