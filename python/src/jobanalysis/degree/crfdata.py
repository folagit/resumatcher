# -*- coding: utf-8 -*-
"""
Created on Fri Nov 07 16:45:45 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from data.labeler import Labeler
from data.jobsentence import JobSentence
from jobaly.match.matcher  import *
from jobaly.match.matchercompiler  import MatcherCompiler

from  data import datautils
from degreelabeler import labeler
from pattern.en import parse, Text, Sentence
from pattern.en import pprint 

sent1 = "BS degree ( BSEE or BSCS strongly preferred , MSCS a plus ) and / or the equivalent in training and experience ."
sent2 = "Bachelor's degree in Computer Science is required."  
sent3 = "He created the robot and broke it after making it."
sent4 = "A Computer Science or related degree. "    
sent5 = "bachelors degree in Computer Science or Information Systems and/or related experience required."    
    

def tagSentence(sent):    
    result = parse(sent,
         tokenize = True,  # Tokenize the input, i.e. split punctuation from words.
             tags = True,  # Find part-of-speech tags.
           chunks = False,  # Find chunk tags, e.g. "the black cat" = NP = noun phrase.
        relations = False,  # Find relations between chunks.
          lemmata = False,  # Find word lemmata.
            light = False)
#    pprint(result)
 
    array = str(result).split(" ")
    tokens = []
    posTags = []
    for a in array:
        b = a.split("/")
        tokens.append(b[0]) 
        posTags.append(b[1]) 
        
  #  print tokens
  #  print posTags
    return (tokens, posTags)

def labelDegreeSet( data_set_name, outfileName ):
    
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")     
    total = 0    
    for item in data:
      #  print item
        sent = item[2]    
     #   sid = item[0]        
        
        print sent 
        labeledSent = labelSent( sent )
      #  print labeledSent.getCrfFormat()
        f.write(labeledSent.getCrfFormat())
        total += 1
        
def labelExampleSet( data_set_name, outfileName, start, end ):
    
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")     
    total = 0    
    r = 100
    for i in range(end-start):
      #  print item
        item = data[i+start]
        sent = item[2]    
     #   sid = item[0]        
        
        print sent 
        labeledSent = labelSent( sent )
      #  print labeledSent.getCrfFormat()
        f.write(labeledSent.getCrfFormat())
        total += 1
        
def labelMajorSet( data_set_name, outfileName, start, num ):
    
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")     
    total = 0    
    r = 100
    i = 0 
    while i < num:
      #  print item
        item = data[i+start]
        sent = item[2]    
     #   sid = item[0]        
        
        print sent 
        labeledSent = labelSent( sent )
      #  print labeledSent.getCrfFormat()
        f.write(labeledSent.getCrfFormat())
        total += 1
        
def labelSent( sent):
    tokens, posTags =  tagSentence(sent)   
    degreeSent = JobSentence(tokens, posTags)
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
    
    return degreeSent 
    

    
def main():       

   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree_crf.txt"
   outfileName = "output\\data3_degree_crf.txt"
  # failfilename =  "output\\data3_degree_array_fail.txt"   
  
 #  labelDegreeSet( target_set_name,outfileName ) 
 #  tagSentence(sent4)  
 #  labeledSent = labelSent( sent4 )
 #  print labeledSent.getCrfFormat()
   trainfile = "output\\data3_100_crf.txt"
   testfile = "output\\data3_200_crf.txt"
 #  labelExampleSet( target_set_name,trainfile, 600, 700 )
   labelMajorSet( target_set_name,testfile, 700, 900 )
   
if __name__ == "__main__": 
    main() 