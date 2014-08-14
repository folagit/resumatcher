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

labeler =  createDegreeLabeler() 

def onlyDegreeLevel(result):
 #   print "result=",result
    newresult = []
    for item in result:
  #      print "item=",item
        if item != [] and \
          labeler.ontoDict.has_key(item):
             newresult.append({labeler.ontoDict[item]:item})
    return newresult
                

matcher1 = LabelMatcher("DE_LEVEL")
matcher2 = LabelMatcher("DEGREE")
degreeSeq1 = SeqMatcher([matcher1,matcher2], outfun=onlyDegreeLevel)

matcher4 = StarMatcher(LabelMatcher([",","DE_LEVEL"]))
matcher5 = QuestionMatcher(LabelMatcher(["OR","DE_LEVEL"]))
degreeSeq2 = SeqMatcher([matcher1,matcher4, matcher5, matcher2], outfun=onlyDegreeLevel)
   
 
matcher10 = LabelMatcher( ["IN"]) + QuestionMatcher(LabelMatcher( [ "DT"])) + LabelMatcher( [ "MAJOR" ])
matcher11 = StarMatcher( LabelMatcher( [",", "MAJOR"] ) )
matcher12 = QuestionMatcher(LabelMatcher( [ "OR" , "MAJOR" ]))
majorseq1 = SeqMatcher([matcher10, matcher11, matcher12] , outfun=onlyDegreeLevel)
 
def getlabeledArray(sent ):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)    
    print degreeSent.printSentenct()  
    labeledArray = degreeSent.getLabeledArray(labelGrammer.ontoDict)
    print degreeSent.printLabeledArray() 
    return labeledArray
 
def getDegreeLevel( matcher , sent ):
    labeledArray = getlabeledArray( sent )
    i = matcher.findMatching(labeledArray)
    return i, matcher.output()

    
def labelDegreeSet(data_set_name, outfileName,failfilename):
     
    data = datautils.loadJson(data_set_name)
    matcher =  degreeSeq2
    matcher = majorseq1
    f = open(outfileName, "w")
    f2 = open(failfilename, "w")
    total = 0
    m = 0
    for item in data:
    #    print item
        sent = item[2]       
       
        degreeSent = JobSentence(sent.split())
        labeler.labelSentence(degreeSent)
     #   print degreeSent.printSentenct()  
    #    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
        labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
    #    print degreeSent.printLabeledArray() 
       
        i = matcher.findMatching(labeledArray)
        print i, matcher.output()
        if i != -1 :
            f.write( sent +"\n\n" )
            f.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f.write( str(i) + "   " + str(matcher.output()) +"\n\n" )
        else :
            f2.write( sent +"\n\n" )
            f2.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f2.write( str(i) + "   " + str(matcher.output()) +"\n\n" )
            
        total += 1
        if i != -1 :
            m+=1
     
    print "match=", m, "  total=", total, "  radio=", float(m)/total

def main(): 
      
   target_set_name = "output\\degree_3"
   outfileName = "output\\degree_3_labe2.txt"
   failfilename =  "output\\degree_3_labe2_fail.txt"
  
   target_set_name = "output\\degree_1"   
   outfileName = "output\\degree_1_layer2.txt"  
   failfilename =  "output\\degree_1_labe2_fail.txt"
   
   target_set_name = "output\\degree_1"   
   outfileName = "output\\degree_1_layer2_major.txt"  
   failfilename =  "output\\degree_1_labe2_fail_major.txt"

   labelDegreeSet(target_set_name,outfileName, failfilename) 
   
if __name__ == "__main__": 
    main() 