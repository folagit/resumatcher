# -*- coding: utf-8 -*-
"""
Created on Sat Aug 02 22:54:28 2014

@author: dlmu__000
"""

from fst  import FstMachine, Alternate
from fst  import *
from drawfst import FstGraph

def test1():
    fst = FstMachine("abc")
    fst = FstMachine(["abc","fff"])
    fst = FstMachine(["a","b","c","d"])
    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test1")
    
def test2():
    item1 = Alternate(["a","b","c"])
    item2 =   ["d","e",item1,"f"] 
    item3 =   Alternate([item1,"d","e"])
    item4 =   ["z","y", item3]
    fst = FstMachine(item4)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test2")
    
def test3():
    item1 = QuestionRepetition(["a","b","c"])
    item2 =  QuestionRepetition("r")
    item3 =   Alternate(["d","e"])
    item4 =   ["z","y", item2]
    item5 =   ["z","y", item2,item3]
    item6 = QuestionRepetition(  Alternate([item1, item2])) 
    fst = FstMachine(item6)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test3")
    
def test4():
    item1 =  ["a","b","c"] 
    item2 =   [item1,item1 ] 
    item3 =   Alternate([item1,item1]) 
    fst = FstMachine(item3)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test4")
    
def test5():
    item1 = PlusRepetition(["a","b","c"])
    item2 =  PlusRepetition("r")
    item3 =   Alternate(["d","e"])
    item4 =   ["z","y", item3, item2]
    item5 =   ["z","y", item2,item3]
    item6 = QuestionRepetition(  Alternate([item1, item2])) 
    fst = FstMachine(item2)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test5")
    
def test6():
    item1 = StarRepetition(["a","b","c"])
    item2 =  StarRepetition("r")
    item3 =   Alternate(["d","e"])
    item4 =   ["z","y", item1]
    item5 =   ["z","y", item2,item3]
    item6 = QuestionRepetition(  Alternate([item1, item2])) 
    fst = FstMachine(item4)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test6")
    
def test7():
    item1 = ["DL", StarRepetition([",","DL"]), QuestionRepetition(["or","DL"]),"DEGREE" ]
     
    fst = FstMachine(item1)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test6")
    
def test8():
    item1 =  ["a","b","c"] 
    item2 =   [item1,item1 ] 
    item3 =   Alternate(["a","a"]) 
    item4 =   Alternate([item3 , item3]) 
    fst = FstMachine(item4)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test8")
    
test8()