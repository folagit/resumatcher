# -*- coding: utf-8 -*-
"""
Created on Sat Aug 02 22:54:28 2014

@author: dlmu__000
"""

from fst  import FstMachine
import fst
from drawfst import FstGraph

def test1():
    fst = FstMachine("abc")
    fst = FstMachine(["abc","fff"])
    fst = FstMachine(["a","b","c","d"])
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test1")
    
test1()