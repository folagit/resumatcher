# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 11:54:58 2014

@author: dlmu__000
"""
from degreelabeler import *
                
#-------- degree matcher ------
matcher1 = LabelMatcher("DE_LEVEL")
matcher2 = LabelMatcher("DEGREE")
degreeSeq1 = SeqMatcher([matcher1,matcher2], outfun=getOntoType)

matcher4 = StarMatcher(LabelMatcher([",","DE_LEVEL"]))
matcher5 = QuestionMatcher(LabelMatcher(["OR","DE_LEVEL"]))
matcher6 = QuestionMatcher(LabelMatcher(["DEGREE_JJ"])) 

# DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)? DEGREE 
degreeSeq2 = SeqMatcher([matcher1,matcher4, matcher5,  matcher2], outfun=getOntoType)

   # we dont need degreeSeq3, result is same
degreeSeq3 = SeqMatcher([matcher1,matcher4, matcher5, matcher6, matcher2], outfun=getOntoType)
 
matcher7 = SeqMatcher(  [ AlternateMatcher ( [ LabelMatcher("IN"), LabelMatcher( "OF" ) ] ), QuestionMatcher(LabelMatcher(["DT"])), LabelMatcher ( "MAJOR") ])  

# DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)? IN|OF (DT)? MAJOR 
degreeSeq4 = SeqMatcher([matcher1,matcher4, matcher5 , matcher7], outfun=getOntoType)
matcher8 = AlternateMatcher([ matcher2, matcher7])  



matcher9 = LabelMatcher("PERFER_VBD")  
matcher10 = AlternateMatcher([ matcher2, matcher7, matcher9])

# DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)? BE? PERFER_VBD   
degreeSeq6 =  matcher1 + matcher4 + matcher5 + QuestionMatcher(LabelMatcher("BE")) +  matcher9
degreeSeq6.outfun=getOntoType

#  "DE_LEVEL (, DE_LEVEL)* (,)? OR DE_LEVEL"
degreeSeq7 = matcher1 + matcher4 + QuestionMatcher(LabelMatcher(",")) +  LabelMatcher(["OR","DE_LEVEL"])
degreeSeq7.outfun=getOntoType

#  DE_LEVEL  |      MAJOR       |    DEGREE 
degreeSeq8 =  matcher1 + LabelMatcher("MAJOR") +  LabelMatcher("DEGREE") 
degreeSeq8.outfun=getOntoType

matcher47 = AlternateMatcher([ LabelMatcher("DE_LEVEL"), LabelMatcher("MAJOR_DE")])
matcher48 = StarMatcher(  SeqMatcher ( [ LabelMatcher(",") , matcher7]))
matcher49 = QuestionMatcher(  SeqMatcher ( [ LabelMatcher("OR") , matcher7]))

degreeSeq41 = SeqMatcher([matcher7,matcher8, matcher9, matcher6, matcher2 ], outfun=getOntoType)


degree_matchers = [ degreeSeq2, degreeSeq4, degreeSeq6, degreeSeq7, degreeSeq8 ] 

def main():       

   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree_array.txt"
   failfilename =  "output\\data3_degree_array_fail.txt"
   
  
   labelDegreeSet(degree_matchers, target_set_name,outfileName, failfilename) 
   
if __name__ == "__main__": 
    main() 
