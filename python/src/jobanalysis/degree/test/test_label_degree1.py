# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 15:45:23 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 00:18:47 2014

@author: dlmu__000
"""
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
 
from degreelabeler import *

 
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

labelGrammer =  createDegreeGrammar()

def onlyDegreeLevel(result):
    print "result=",result
    newresult = []
    for item in result:
        print "item=",item
        if item != [] and \
          labelGrammer.ontoDict.has_key(item):
            newresult.append(item)
    return newresult
                

matcher1 = LabelMatcher("DE_LEVEL")
matcher2 = LabelMatcher("DEGREE")
degreeSeq1 = SeqMatcher([matcher1,matcher2], outfun=onlyDegreeLevel)

matcher4 = StarMatcher(LabelMatcher([",","DE_LEVEL"]))
matcher5 = QuestionMatcher(LabelMatcher(["OR","DE_LEVEL"]))
degreeSeq2 = SeqMatcher([matcher1,matcher4, matcher5, matcher2], outfun=onlyDegreeLevel)
   

matcher10 = LabelMatcher( [ "IN" , "MAJOR" ])
matcher11 = StarMatcher( LabelMatcher( [",", "MAJOR"] ) )
matcher12 = LabelMatcher( [ "OR" , "MAJOR" ])
matcher13 = SeqMatcher([matcher10, matcher11, matcher12])
 
def getlabeledArray(sent ):
    degreeSent = JobSentence(sent.split())
    labelGrammer.labelSentence(degreeSent)
    print degreeSent.printSentenct()  
    labeledArray = degreeSent.getLabeledArray(labelGrammer.ontoDict)
    print degreeSent.printLabeledArray() 
    return labeledArray
    

class TestLabelDegree1(unittest.TestCase):    

    def test_label1(self):        
        labeledArray =  getlabeledArray(sent02 ) 
        i = degreeSeq1.findMatching(labeledArray)    
        self.assertEqual(i,0)
        self.assertEqual(degreeSeq1.output(),['BS_LEVEL'])    
        
        
    def test_label2(self):        
        labeledArray =  getlabeledArray(sent10 ) 
        i = degreeSeq2.findMatching(labeledArray)    
        self.assertEqual(i,0)
        self.assertEqual(degreeSeq2.output(),['BS_LEVEL', 'MS_LEVEL'])  
 #       print degreeSeq2.getFound(labeledArray)
   
       
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLabelDegree1)
    unittest.TextTestRunner(verbosity=2).run(suite)

 