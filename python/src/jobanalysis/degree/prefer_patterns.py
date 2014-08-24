# -*- coding: utf-8 -*-
"""
Created on Sat Aug 23 13:46:59 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 17:22:23 2014

@author: dlmu__000
"""

from degreelabeler import *



#-------- major matcher ------

# （IN| OF) DT? MAJOR
prefer_01 =    LabelMatcher( [ "MAJOR", "DEGREE", "PREFER_VBD"] )
prefer_02 =    LabelMatcher( [   "DEGREE", "IN", "MAJOR", "PREFER_VBD"] )
prefer_03 =    LabelMatcher( [   ",", "MAJOR_DEGREE", "PREFER_VBD"] )
prefer_04 =    LabelMatcher( [   ",", "MAJOR", "PREFER_VBD"] )
prefer_05 =    LabelMatcher( [   "PREFER_VBD" , "IN", "MAJOR" ] )
prefer_06 =    LabelMatcher( "DE_LEVEL" ) + QuestionMatcher(LabelMatcher("DEGREE")) + QuestionMatcher(DotMatcher()) + QuestionMatcher(LabelMatcher("BE"))  + AlternateMatcher([LabelMatcher("PREFER_VBD"), LabelMatcher("PREFER_NN") ,  LabelMatcher("PREFER_JJ")  ]) 
prefer_07 =    LabelMatcher(    "PREFER_VBD" ) +  QuestionMatcher(LabelMatcher("EDUCATION")) + LabelMatcher( [ ":", "DE_LEVEL"] )
prefer_08 =    LabelMatcher(   "PREFER_VBD" ) +  QuestionMatcher(LabelMatcher("DT" ))  +   LabelMatcher( "DE_LEVEL" )   + LabelMatcher( "DEGREE" )
prefer_09 =    LabelMatcher( [  "DEGREE", "IN", "MAJOR", "PREFER_VBD"] )
prefer_10 =    LabelMatcher( ["DE_LEVEL", "DEGREE", "BE", "PREFER_JJ"])

prefer_matchers = [prefer_01, prefer_02,prefer_03, prefer_04, prefer_05 , \
               prefer_06, prefer_07, prefer_08 , prefer_09, prefer_10]
def main(): 
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_PREFER_array.txt"
   failfilename =  "output\\data3_PREFER_array_fail.txt"   
   
   
   labelDegreeSet(prefer_matchers, target_set_name,outfileName, failfilename) 
   
if __name__ == "__main__": 
    main() 