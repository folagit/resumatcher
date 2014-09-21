# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 18:05:18 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import modelsimilarity

def test_tranferDegree():
    degrees = set(["AS_LEVEL",  "BS_LEVEL", "MS_LEVEL", "GRAD_LEVEL"])
    degreeNum = modelsimilarity.tranferDegree(degrees)
    for num in  degreeNum:
        print num
        

test_tranferDegree()    