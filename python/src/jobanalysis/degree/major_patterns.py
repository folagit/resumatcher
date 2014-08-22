# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 17:22:23 2014

@author: dlmu__000
"""

from degreelabeler import *

labeler =  createDegreeLabeler() 
def getOntoType(result):
 #   print "result=",result
    newresult = []
    for item in result:
     #   print " ^item=",item
        if item != [] and \
          labeler.ontoDict.has_key(item):
             newresult.append({labeler.ontoDict[item]:item})
    return newresult

#-------- major matcher ------

# （IN| OF) DT? MAJOR
matcher101 =  AlternateMatcher( [ LabelMatcher( "IN" ), LabelMatcher( "OF" )])  + QuestionMatcher(LabelMatcher( [ "DT"])) + LabelMatcher( [ "MAJOR" ])

# (, MAJOR)* 

matcher102 = StarMatcher(  LabelMatcher( [",", "MAJOR"]  ) )

# (, MAJOR)* 
matcher103 = QuestionMatcher(LabelMatcher( [ "OR" , "MAJOR" ]))

#IN DT? MAJOR (, MAJOR)* OR　MAJOR
majorSeq1 =  matcher101 + matcher102 + matcher103 
majorSeq1.outfun=getOntoType


