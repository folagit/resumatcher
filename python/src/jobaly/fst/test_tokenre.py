# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 01:09:21 2014

@author: dlmu__000
"""

 
from tokenre  import *
from drawfst import FstGraph

def test1():
    fst1 = TokenRegex("abc")
    fst2 = TokenRegex(["abc","fff"])
    fst3 = TokenRegex(["a","b","c","d"])
    
    grapth = FstGraph(fst3)
    grapth.draw("outfiles//test_tokenre_1")
    
def test2():
    item1 = Alternate(["a","b","c"])
    item2 =   ["d","e",item1,"f"] 
    item3 =   Alternate([item1,"d","e"])
    item4 =   ["z","y", item3,"x","o"]
    item5 =   Alternate(["z","y" , "x","o"])
    item6 = [item1, item5]
    fst = TokenRegex(item2)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test2")
    
def test3():
    item1 = QuestionRepetition(["a","b","c"])
    item2 =  QuestionRepetition("r")
    item3 =    ["d","e", item1,"f" ]
    item4 =   ["z","y", item2]
    item5 =   ["z","y", item1,item2]
    item6 = QuestionRepetition(  Alternate([item1, item2]))
    item7 = [ "a", "b", Alternate(["c","d",""]) ,"e"]
    fst = TokenRegex(item7)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test3")
    
def test4():
    item1 =  ["a","b","c"] 
    item2 =   [item1,item1 ] 
    item3 =   Alternate([item1,item1]) 
    fst = TokenRegex(item3)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test4")
    
def test5():
    item1 = PlusRepetition(["a","b","c"])
    item2 =  PlusRepetition("r")
    item3 =   Alternate(["d","e"])
    item4 =   ["z","y", item3, item2]
    item5 =   ["z","y", item2, item3]
    item6 = QuestionRepetition(  Alternate([item1, item2])) 
    fst = TokenRegex(item1)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test5")
    
def test6():
    item1 = StarRepetition(["a","b","c"])
    item2 =  StarRepetition("r")
    item3 =   Alternate(["d","e"])
    item4 =   ["z","y", item1,"x"]
    item5 =   ["z","y", item2,item3]
    item6 = QuestionRepetition(  Alternate([item1, item2])) 
    fst = TokenRegex(item5)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test6")
    
def test7():
    item1 = ["DL", StarRepetition([",","DL"]), QuestionRepetition(["or","DL"]),"DEGREE" ]
     
    fst = TokenRegex(item1)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test6")
    
def test8():
    item1 = Alternate(["a","b"])     
    item2 = QuestionRepetition(Alternate(["d","e" ]))  
    item3 = StarRepetition(["f","g" ])    
    item4 = PlusRepetition(["h","i" ])
    
    item8 = [item1,item2, item3, item4]
    
    fst = TokenRegex(item8)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test8")
    
def test9():
    item1 =  ["a","b","c"] 
    item2 =   [item1,item1 ] 
    item3 =   Alternate(["a","a"]) 
    item4 =   Alternate([item3 , item3]) 
    fst = TokenRegex(item4)    
    grapth = FstGraph(fst)
    grapth.draw("outfiles//test9")
    
test9()