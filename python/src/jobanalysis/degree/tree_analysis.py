# -*- coding: utf-8 -*-
"""
Created on Sat Jul 26 22:28:06 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 16:27:50 2014

@author: dlmu__000
"""

from practnlptools.tools import Annotator
from nltk.tree import Tree

from pattern.en import parse, Text, Sentence
from pattern.en import pprint, parsetree

sent01 = "bachelors degree"
sent02 = "bachelors Degree preferred"
sent03 = "Bachelors Degree or Equivalent"
sent04 = "bachelors degree in Computer Science"
sent05 = "bachelors degree in Computer Science or equivalent"    
sent06 = "B.S. degree in Computer Science required" 
sent07 = "Requires a Bachelors degree in Information Systems or related field"
sent08 = "Bachelors degree in computer science or an equivalent combination of education and/or experience"
sent09 = "bachelors degree in related field , OR four ( 4 ) years of experience in a directly related field"
sent10 = "Bachelors or master degree in computer science" 
sent11 = "Bachelor , Master or Doctorate of Science degree from an accredited course of study , in engineering , computer science , mathematics , physics or chemistry"
    
 
    
def draw_tree():   
    
    
    annotator=Annotator()
    result = annotator.getAnnotations(sent11)
    tree_str = result['syntax_tree']
    print     
   # print tree_str
    
    tree = Tree.fromstring(tree_str)[0]
    print tree.pprint()
    print
    print "Root label=",tree.label()
    tree.draw()

def printChunk(chunk):
    
      print "---------------------------------------"
      print  "chunk :",  chunk
      print  "words :", chunk.words 
      print  "tagged:" , chunk.tagged          
      
      print  "chunk :" , chunk.type
      print  "relations", chunk.relations
      print  "head:", chunk.head
      print  "pnp:" , chunk.pnp
      print  "relation: " ,  chunk.relation
      print  "role: " ,  chunk.role
      print  "related" , chunk.related
      print "---------------------------------------"
    
    
def patternTree():
    
    s = parsetree(sent11) 
    for sentence in s: 
       for chunk in sentence.chunks:
           printChunk(chunk)
           
  
patternTree()

