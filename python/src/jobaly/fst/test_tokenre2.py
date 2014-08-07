# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 22:32:03 2014

@author: dlmu__000
"""
from tokenre  import *
from drawfst import FstGraph
from prettytable import PrettyTable

def printTrack(track):       
    x = PrettyTable(["state","last", "i", "j", "token"])   
  
    for  state, last , j, i  in   track:
           x.add_row([state._id, last._id, i, j,  state.matcher ])     
                    
           
    print x.get_string()

def test1():
    tokens = ["aaa","bbb","ccc","ddd"]    
    
    pattern1 = "aaa"
    pattern2 = "bbb"
    pattern3 = ["bbb","ccc"]
    pattern4 = "ddd"
    pattern5 = "eee"
    
    fst = TokenRegex(pattern4) 
    track =  fst._match(tokens) 
    printTrack(track)
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_1")
    
def test2():
    tokens = ["aaa","bbb","ccc","ddd"]    
    
    pattern1 = Alternate(["ccc","fff"])
   
    pattern2 = [ "bbb", pattern1 ]
    pattern3 = [pattern2,"ggg"]
    pattern4 = "ddd"
    pattern5 = "eee"
    
    fst = TokenRegex(pattern3) 
 #   track =  fst._match(tokens) 
 #   printTrack(track)
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_1")
    
test2()