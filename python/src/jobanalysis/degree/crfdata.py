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

def labelDegreeSet(matchers, data_set_name, outfileName,failfilename):
   
    for matcher in matchers:       
            matcher.matchNum = 0     
     
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")
    f2 = open(failfilename, "w")
    total = 0
    m = 0
    for item in data:
    #    print item
        sent = item[2]    
        sid = item[0]         
        matcher = None
        degreeSent, matcher = labelSentByMatchers(matchers, sent) 
     
        if matcher is not None:
            output = matcher.output()
            found = matcher.found
        else:
            output = None
            found = None
        
        print sid ,found, output 
        total += 1
        if matcher is not None :
            m+=1
            f.write( sent +"\n\n" )
            f.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f.write( str(found) + "   " + str(output) +"\n\n" )
        else :
            f2.write( sent +"\n\n" )
            f2.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
             
    f2.write( "\n\n match="+ str( m) + "  total="+ str( total) + "  radio=" + str (float(m)/total) +"\n" )
             
    print "match=", m, "  total=", total, "  radio=", float(m)/total
    
    i = 0
    for matcher in matchers :
        i+=1
        print "matcher ", i, ":", matcher.matchNum
        f2.write( "\n matcher " + str( i) + ":" + str( matcher.matchNum ) )


def labelSent( sent):
    tokens, posTags =  tagSentence(sent4)   
    degreeSent = JobSentence(tokens, posTags)
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
    
    return degreeSent 
    

    
def main():       

   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree_array.txt"
   failfilename =  "output\\data3_degree_array_fail.txt"   
  
  # labelDegreeSet(degree_matchers, target_set_name,outfileName, failfilename) 
 #  tagSentence(sent4)  
   labeledSent = labelSent( sent4 )
   print labeledSent.getCrfFormat()
   
if __name__ == "__main__": 
    main() 