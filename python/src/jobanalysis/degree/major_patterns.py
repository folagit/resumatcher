# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 17:22:23 2014

@author: dlmu__000
"""

from degreelabeler import *



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


matcher111 = LabelMatcher(  "MAJOR"   )
matcher112 = QuestionMatcher( LabelMatcher(  "DE_LEVEL" ) )
matcher113 = LabelMatcher(  "DEGREE"   )
majorSeq2 =  matcher111 + matcher112 + matcher113 

majorSeq3 =  LabelMatcher( "MAJOR") + matcher102 + LabelMatcher( [ "OR" , "MAJOR" ])
majorSeq4 =  LabelMatcher( "MAJOR") + matcher102 + LabelMatcher( [",", "MAJOR"]  )

matcher116 = LabelMatcher( "MAJOR_DEGREE")
majorSeq5 = LabelMatcher( "MAJOR_DEGREE") + StarMatcher(LabelMatcher( [",","MAJOR_DEGREE"])) +  QuestionMatcher( LabelMatcher( [ "OR" , "MAJOR" ]))

majorSeq6 = LabelMatcher( "MAJOR") + DotMatcher() +   DotMatcher() + LabelMatcher( "DEGREE")

majorSeq7 = LabelMatcher( "PERFER_VBD") + LabelMatcher( "MAJOR")
majorSeq8 = LabelMatcher( "MAJOR") + LabelMatcher( "PERFER_VBD") 

majorSeq9 =  LabelMatcher( "MAJOR") + OriTextMatcher(["or" , "related"])

majorSeq10 =   LabelMatcher(  "DEGREE"   ) + DotMatcher() + LabelMatcher( "MAJOR") 

major_matchers = [majorSeq1, majorSeq2, majorSeq3,majorSeq4, majorSeq5, \
               majorSeq6, majorSeq7, majorSeq8, majorSeq9, majorSeq10 ]
def main(): 
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_major_array.txt"
   failfilename =  "output\\data3_major_array_fail.txt"   
   
   
   labelDegreeSet(major_matchers, target_set_name,outfileName, failfilename) 
   
if __name__ == "__main__": 
    main() 