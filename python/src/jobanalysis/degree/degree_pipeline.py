# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 12:29:07 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from data.jobsentence import JobSentence
from jobaly.match.matcher  import *

from  data import datautils
from degreelabeler import *

import major_patterns
import prefer_patterns
import degree_patterns

def extractInfo(sent):
  
    degreeModel = []    
    
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
#    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    matcher =  matchSent(degree_patterns.degree_matchers, labeledArray)
    if matcher is not None:
        output = matcher.output()
        degreeModel.extend(output)
        
    matcher =  matchSent(major_patterns.major_matchers, labeledArray)
    if matcher is not None:
        output = matcher.output()
        degreeModel.extend(output)
        
    matcher =  matchSent(prefer_patterns.prefer_matchers, labeledArray)
    if matcher is not None:
        output = matcher.output()
        degreeModel.extend(output)
        
    return degreeSent, degreeModel 
    
def processDegreeSet(data_set_name, outfileName,failfilename):
     
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")
    f2 = open(failfilename, "w")
    total = 0
    m = 0
    for item in data:
    #    print item
        sent = item[2]    
        sid = item[0]         
       
        degreeSent, degreeModel = extractInfo(sent) 
        
        print sid , degreeModel
        if len(degreeModel) > 0 :
            m+=1
            f.write( sent +"\n\n" )
            f.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f.write( str(degreeModel)   +"\n\n" )
        else :
            f2.write( sent +"\n\n" )
            f2.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            
            
        total += 1
        
            
    f2.write( "\n\n match="+ str( m) + "  total="+ str( total) + "  radio=" + str (float(m)/total) )
             
    print "match=", m, "  total=", total, "  radio=", float(m)/total

def main(): 
      
   target_set_name = "output\\degree_3"
   outfileName = "output\\degree_3_model.txt"
   failfilename =  "output\\degree_3_model_fail.txt"
   
   processDegreeSet( target_set_name,outfileName, failfilename) 

if __name__ == "__main__": 
    main() 