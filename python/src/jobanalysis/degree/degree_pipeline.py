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
     #   print " ^item=",item
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
   
matcher6 = QuestionMatcher(LabelMatcher(["DEGREE_JJ"])) 
matcher7 = AlternateMatcher([ LabelMatcher("DE_LEVEL"), LabelMatcher("MAJOR_DE")])
matcher8 = StarMatcher(  SeqMatcher ( [ LabelMatcher(",") , matcher7]))
matcher9 = QuestionMatcher(  SeqMatcher ( [ LabelMatcher("OR") , matcher7]))

degreeSeq3 = SeqMatcher([matcher7,matcher8, matcher9, matcher6, matcher2 ], outfun=onlyDegreeLevel)

matcher10 = LabelMatcher( ["IN"]) + QuestionMatcher(LabelMatcher( [ "DT"])) + LabelMatcher( [ "MAJOR" ])
matcher11 = StarMatcher( AlternateMatcher( [ LabelMatcher( [",", "MAJOR"] ), LabelMatcher(   "MAJOR" )]  ) )
matcher12 = QuestionMatcher(LabelMatcher( [ "OR" , "MAJOR" ]))
majorseq1 = SeqMatcher([matcher10, matcher11, matcher12] , outfun=onlyDegreeLevel)
 

def labelSent(matcher, sent):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
#    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    i = matcher.findMatching(labeledArray) 
    return i, degreeSent  
    
def labelDegreeSet(matcher, data_set_name, outfileName,failfilename):
     
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")
    f2 = open(failfilename, "w")
    total = 0
    m = 0
    for item in data:
    #    print item
        sent = item[2]    
        sid = item[0]         
       
        i, degreeSent = labelSent(matcher, sent) 
        
        print sid ,i, matcher.output()
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
  
   matcher =  degreeSeq2   
   target_set_name = "output\\degree_1"   
   outfileName = "output\\degree_1_layer2.txt"  
   failfilename =  "output\\degree_1_labe2_fail.txt"

   
   matcher = majorseq1
   target_set_name = "output\\degree_1"   
   outfileName = "output\\degree_1_layer2_major.txt"  
   failfilename =  "output\\degree_1_labe2_fail_major.txt"
   
   matcher = majorseq1
   target_set_name = "output\\degree_1"   
   outfileName = "output\\degree_1_layer2_major.txt"  
   failfilename =  "output\\degree_1_labe2_fail_major.txt"
 

   matcher =  degreeSeq2  
 #  matcher =  degreeSeq3
  # matcher = matcher7
   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree1.txt"  
   failfilename =  "output\\data1_degree1_fail.txt"
    
  
   

   labelDegreeSet(matcher, target_set_name,outfileName, failfilename) 
   


if __name__ == "__main__": 
    main() 