# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 16:15:19 2014

@author: dlmu__000
"""

import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

 
from degreelabeler import *
from degree_pipeline import * 

sent10 = "Bachelor , Master or Doctorate  degree from an accredited course of study"
sent11 = "Bachelor , Master or Doctorate  degree from an accredited course of study , in engineering , computer science , mathematics , physics or chemistry"
sent12 = "BSCS , BSEE Degree ( transcripts required )"

def test1():
    
    matcher = degreeSeq3
 #   matcher = degreeSeq2
    i, degreeSent = labelSent(matcher, sent12)   
    print degreeSent.printLabeledArray()         
    print i, matcher.output()
    print i, matcher.catch
    print "outlist=", matcher.outlist
    
test1()