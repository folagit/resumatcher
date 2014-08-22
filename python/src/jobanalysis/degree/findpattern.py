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

from data.jobsentence import JobSentence
from degreelabeler import *
from degree_patterns import *
from major_patterns import *


def labelSentByMatchers(matchers, sent):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
#    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    i, output =  matchSent(matchers, labeledArray)
    return i, degreeSent, output 

def matchSent(matchers, labeledArray):
    
    for matcher in matchers:
        i = matcher.findMatching(labeledArray) 
        if i != -1:
            matcher.matchNum += 1
            return i, matcher.output()
            
    return i, None
    
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
       
        i, degreeSent, output = labelSentByMatchers(matchers, sent) 
        
        print sid ,i, output 
        if i != -1 :
            f.write( sent +"\n\n" )
            f.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f.write( str(i) + "   " + str(output) +"\n\n" )
        else :
            f2.write( sent +"\n\n" )
            f2.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f2.write( str(i) + "   " + str(output) +"\n\n" )
            
        total += 1
        if i != -1 :
            m+=1
            
    f2.write( "\n\n match="+ str( m) + "  total="+ str( total) + "  radio=" + str (float(m)/total) +"\n" )
             
    print "match=", m, "  total=", total, "  radio=", float(m)/total
    
    i = 0
    for matcher in matchers :
        print "matcher ", i, ":", matcher.matchNum
        f2.write( "\n matcher " + str( i) + ":" + str( matcher.matchNum ) )
    

def main(): 
      
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree1.txt"
   failfilename =  "output\\data3_degree1_fail.txt"

   matcher =  degreeSeq8  
 #  matcher =  degreeSeq3
  # matcher = matcher7
   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree1.txt"  
   failfilename =  "output\\data1_degree1_fail.txt"
   
   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree5.txt"  
   failfilename =  "output\\data1_degree5_fail.txt"
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree5.txt"
   failfilename =  "output\\data3_degree5_fail.txt"

   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree6.txt"  
   failfilename =  "output\\data1_degree6_fail.txt"
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree6.txt"
   failfilename =  "output\\data3_degree6_fail.txt"
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree_array.txt"
   failfilename =  "output\\data3_degree_array_fail.txt"
   
   matchers = [ degreeSeq2, degreeSeq4, degreeSeq6, degreeSeq7, degreeSeq8 ]   
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_major_array.txt"
   failfilename =  "output\\data3_major_array_fail.txt"   
   
   matchers = [majorSeq1]

   labelDegreeSet(matchers, target_set_name,outfileName, failfilename) 
   


if __name__ == "__main__": 
    main() 