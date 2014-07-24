# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 16:27:50 2014

@author: dlmu__000
"""

from practnlptools.tools import Annotator

def test1():
    annotator=Annotator()
    sent = "There are people dying make this world a better place for you and for me."
    result = annotator.getAnnotations(sent)

    #print result
    print type (result)
    print  result.keys()   

def test2(): 
    sent = "There are people dying make this world a better place for you and for me."
    
    annotator=Annotator()    
    result = annotator.getAnnotations(sent,dep_parse=True)
    print  result
    
def test3():
    annotator=Annotator()
    sent = "There are people dying make this world a better place for you and for me."
    sent = "Biplab is a good boy." 
    sent = "He created the robot and broke it after making it."
    result = annotator.getAnnotations(sent)

    print result["pos"]
    print result['ner']
    print result['chunk']
    print result['verbs']
    print result['srl']
  
def test_tree():
    annotator=Annotator()
    sent = "There are people dying make this world a better place for you and for me."
    sent = "Biplab is a good boy." 
    sent = "He created the robot and broke it after making it."
    result = annotator.getAnnotations(sent)

    print result['syntax_tree']
    
def test_deep():
    annotator=Annotator()
    sent = "There are people dying make this world a better place for you and for me."
    sent = "Biplab is a good boy." 
    sent = "He created the robot and broke it after making it."
    result = annotator.getAnnotations(sent,dep_parse=True)

    print result['dep_parse']
    
test_deep()

