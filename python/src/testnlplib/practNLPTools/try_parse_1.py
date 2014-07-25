# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 16:27:50 2014

@author: dlmu__000
"""

from practnlptools.tools import Annotator
from nltk.tree import Tree

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
    
def test_tree2():
    
    
    annotator=Annotator()
    sent = "There are people dying make this world a better place for you and for me."
    sent = "Biplab is a good boy." 
    sent = "He created the robot and broke it after making it."
    sent = "Bachelor 's degree in computer science , design or related field."    
    result = annotator.getAnnotations(sent)
    tree_str = result['syntax_tree']
    print result['syntax_tree']
    print "--------------------"
    tree2 = Tree(tree_str)
    print len(tree2)   
    print "--------------------"
    
    for item in tree2[0]:
        print type(item)
        print item
        
def test_tree3():
    tree_str = "(S1(S(NP(PRP He))(VP(VP(VBD created)(NP(DT the)(NN robot)))(CC and)(VP(VBD broke)(NP(PRP it))(PP(IN after)(S(VP(VBG making)(NP(PRP it.)))))))))"
    tree = Tree.fromstring(tree_str)[0]
    print type(tree)
    print tree.label()
    tree.draw()
    
def test_tree4():   
    
    annotator=Annotator()
    sent = "There are people dying make this world a better place for you and for me."
    sent = "Biplab is a good boy." 
    sent = "He created the robot and broke it after making it."
    sent = "Bachelor 's degree in computer science , design or related field."    
    sent = "B.S. in Computer Science , a related degree or its equivalent"    
    sent = "BS , MS , or PhD in Computer Science or a similar field preferred"
    sent = "Computer Science or related technical degree from an accredited four year university "
    sent = "Degree in Computer Science or Engineering with a high GPA ."    
    sent = "A Master's degree in Computer Science or Engineering is mandatory ."
    result = annotator.getAnnotations(sent)
    tree_str = result['syntax_tree']
    print     
    print tree_str
    
    tree = Tree.fromstring(tree_str)[0]
    print
    print "Root label=",tree.label()
    tree.draw()
  
test_tree4()

