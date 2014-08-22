# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 00:53:20 2014

@author: dlmu__000
"""

import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

 
from degreelabeler import *
from major_patterns import *

sent1 = "BSCS , BSEE Degree ( transcripts required )"
sent2 = "A BS in a computer science , programming or IT related degree would be preferred ."
sent3 = "A BS in a computer science , programming or IT "
sent4 = "Bachelors degree in Electronic Engineering or related field "
sent5 = "BSCS or BSEE or other Related 4-yr Technical Degree preferred ."
sent6 = "Computer science or related degree"

def test1():

    matcher = majorSeq6
 #   matcher = degreeSeq2
    i, degreeSent = labelSent(labeler, matcher, sent6)   
    print degreeSent.printLabeledArray()         
    print i, matcher.output()
    print i, matcher.catch
    print "outlist=", matcher.outlist
    
test1()