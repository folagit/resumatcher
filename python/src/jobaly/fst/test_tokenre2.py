# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 22:32:03 2014

@author: dlmu__000
"""
from tokenre  import *
from drawfst import FstGraph
from prettytable import PrettyTable

def printTrack(track):       
    x = PrettyTable(["state", "i", "j","matcher","token"])   
  
    for  state , j, i  in   track:  
       if j != -1 : 
           matcher = state.outStates[j] 
           x.add_row([state._id, i, j, matcher._id, matcher.matcher ])     
        # x.add_row([state._id, i, j, "","" ])  
       else :
           x.add_row([state._id, i, j, "","" ])                
           
    print x.get_string()

def test1():
    tokens = ["aaa","bbb","ccc","ddd"]    
    
    pattern1 = "aaa"
    pattern2 = "bbb"
    pattern3 = ["bbb","ccc"]
    pattern4 = "ddd"
    pattern5 = "eee"
    
    fst = TokenRegex(pattern5) 
    track =  fst._match(tokens) 
    printTrack(track)
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_1")
    
test1()