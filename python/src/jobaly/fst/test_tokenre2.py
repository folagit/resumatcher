# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 22:32:03 2014

@author: dlmu__000
"""
from tokenre  import *
from drawfst import FstGraph


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
    tokens = ["000","aaa","bbb","aaa","bbb","ccc","ddd","eee"]    
    
    pattern1 = Alternate(["ccc","fff"])   
    pattern2 = [ "bbb", pattern1 ]
    pattern3 = [pattern2,"ggg"]
    
    pattern4 = ["bbb","ccc"]
    pattern5 = Alternate([pattern4,"bbb"]) 
    pattern6 = Alternate(["bbb",pattern4])
    pattern7 = Alternate([ ["bbb","ddd"],pattern4])
    pattern8 = ["aaa", Alternate([pattern3, pattern7 ]) ,"ddd" ]
    
    fst = TokenRegex(pattern8) 
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_2")
    
    track =  fst._match(tokens) 
    print "==================================="
    printTrack(track)
    
def test3():
    tokens = ["bbb","aaa","bbb","ccc","ddd","eee"]    
    
    pattern1 = QuestionRepetition(["bbb","ccc"])   
    pattern2 = [ "aaa", pattern1,"ddd" ]
    pattern3 = [ "aaa", pattern1,"ccc" ]
    pattern4 = [ "aaa", pattern1,"bbb" ]
   
    pattern5 = Alternate([pattern4,"bbb"]) 
    pattern6 = Alternate(["bbb",pattern4])
    pattern7 = Alternate([ ["bbb","ddd"],pattern4])
    pattern8 = [ QuestionRepetition(Alternate([pattern3, pattern4 ])) ,"ddd" ]
    
    fst = TokenRegex(pattern8) 
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_3")
    
    track =  fst._match(tokens) 
    print "==================================="
    printTrack(track)   
    
def test4():
    tokens = ["000","aaa","bbb","aaa","bbb","ccc","ddd","eee"]    
    
    pattern1 = PlusRepetition(["ccc","fff"])   
    pattern2 = PlusRepetition(["aaa","bbb"])   
    pattern3 = ["bbb",pattern2]
    
    pattern4 = [pattern2,"ccc"]
    
    fst = TokenRegex(pattern4) 
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_4")
    
    track =  fst._match(tokens) 
    print "==================================="
    printTrack(track)
    
def test5():
    tokens = [ "aaa","bbb","aaa","bbb","ccc","ddd","eee"]    
    
    pattern1 = StarRepetition(["ccc","fff"])   
    pattern2 = StarRepetition(["aaa","bbb"])   
    pattern3 = ["bbb",pattern2]
    
    pattern4 = [pattern2,"ccc"]
    
    fst = TokenRegex(pattern4) 
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_5")
    
    track =  fst._match(tokens) 
    print "==================================="
    printTrack(track)
    
def test6():
    tokens = [ "aaa","bbb" ]    
    
    pattern1 =  [ "aaa","bbb"]    
    pattern2 =  [ "aaa","bbb","ccc"]    
    pattern3 = Alternate([ pattern2 , [ "bbb"] ])
    
    pattern4 = [pattern1,"ccc"]
    
    fst = TokenRegex(pattern4) 
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test_tokenre2_6")
    
    track =  fst._match(tokens) 
    print "==================================="
    printTrack(track)
    
test6()