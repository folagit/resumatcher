# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 15:36:48 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 20:31:27 2014

@author: dlmu__000

"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


from data.labeler import Labeler
from data.jobsentence import JobSentence
from jobaly.match.matcher  import *

def addLabels(labelDict, items, label):
    for item in items:
        labelDict[item] = label
        
def createLabelDict():
    labelDict = {  "or": "OR", "OR": "OR", "and" : "AND" ,  "in": "IN" , "In":"IN" , \
           "of" : "OF", "and/or" : "AND_OR", "from" :"FROM" , "with":"WITH" , \
           "at":"AT" ,"about":"ABOUT" , "for" : "FOR" ,"as":"AS" }
    BE = ["Be","be", "is", "are", "was", "were", "am"]    
    DT = ["a", "A", "an", "An", "The", "the"]  
    DIGIT = ['one', "two", "three", "four", "five", "seven", "eight", "night", "ten" ]
    YEAR = ["year", "years", "yr"]
    
    addLabels(labelDict, BE, "BE" )  
    addLabels(labelDict, DT, "DT" )  
    addLabels(labelDict, DIGIT, "DIGIT" )  
    addLabels(labelDict, YEAR, "YEAR" )
    
    return labelDict
   
def addMoreLabels(labelDict):      
   
    DEGREE = ["degree","degrees"]
    HS_LEVEL = ["High School Diploma", "High School" ,"GED"]    
    AS_LEVEL = ["AS","Associate","Associates", "AA", "A.A."]
    BS_LEVEL = ["Baccalaureate","bachelors", "bachelor" ,"B.S.","BS","BA","BA/BS", "BABS", "B.A." ,"4-year","4-year", "four year","college","Undergraduate" , "University" ]    
    MS_LEVEL = ["masters", "MS", "M.S.", "master", "MA" , "MSc"]
    PHD_LEVEL = ["PhD", "Ph.D", "doctorate" ]
    MS_PHD_LEVEL = ["Graduate", "advanced" ]
    DEGREE_JJ = [ "similar", "related","Relevant", "equivalent" ]
    MAJOR = ["computer science", "CS", "CE" ,"EE", "IS", "computer engineering", "Information Systems",  \
         "Digital Media", "Information Technology","Software Engineering", "computer programming" ,"statistics", \
         "Applied Mathematics", "mathematics", "biological sciences", "Physics", "math" , "chemistry" , \
         "signal processing","Electrical Engineering ", "Information Sciences","MIS", "CIS", "GIS" , "IT", "Telecom" , "Computing Science " , "Technology Management" , "Technology",
         "Marketing", "Business", "Finance" , "Economics", "accounting",        
         "Web Development","Web Design",  "Communications", "Communication Sciences","Interactive Design"   , "Journalism",        
         "related field" , "related discipline", "related area"
         "relevant discipline" ,  "related discipline" ,"related subject", "relevant subject" ]
                            
    MAJOR_DEGREE = ["MBA", "BSCS", "BSEE", "MSCS", "MSEE" ]
    MAJOR_WEAK = ["engineering", "science", "Management", "design", "technical" ]
   
    PERFER_RB = ["preferably"]  
    PERFER_NN = [ "a plus", "at least" ]
    PERFER_VBD = ["preferred", "required","desired" ]    
    PERFER_JJ = [ "plus", "minimum", "mandatory","desirable"]    
    PERFER_VB =  ["Requires" , "have", "Pursuing", "Prefer"]
    MD = ["must", "should","would"]
    HIGHER_JJ = ["above", "higher","greater","better"]
    
    EXPERIENCE = ["experience" , "work experience" , "practical experience" ,"professional experience" ]
    EDUCATION = ["education"]
    
    QUALIFICATION = ["Qualifications", "Qualification"]
    APPLICANT = [ "Applicant" ,"Applicants" ,"candidate"]
    
   
    addLabels(labelDict, DEGREE, "DEGREE" )    
    
    addLabels(labelDict, MAJOR, "MAJOR" )
    addLabels(labelDict, MAJOR_DEGREE, "MAJOR_DE" )
    
    addLabels(labelDict, EXPERIENCE, "EXPERIENCE" )
    addLabels(labelDict, EDUCATION, "EDUCATION" )
    
    addLabels(labelDict, DEGREE_JJ, "DEGREE_JJ" )
    
    addLabels(labelDict, PERFER_RB, "PERFER_RB" )
    addLabels(labelDict, PERFER_NN, "PERFER_NN" )
    addLabels(labelDict, PERFER_VBD, "PERFER_VBD" )
    addLabels(labelDict, PERFER_JJ, "PERFER_JJ" )
    addLabels(labelDict, PERFER_VB, "PERFER_VB" )
    addLabels(labelDict, MAJOR_WEAK, "MAJOR" )
    addLabels(labelDict, HIGHER_JJ, "HIGHER_JJ" )
    addLabels(labelDict, MD, "MD" )
    addLabels(labelDict, QUALIFICATION, "QUALIFICATION" )
    addLabels(labelDict, APPLICANT, "APPLICANT" )
    
    addLabels(labelDict, HS_LEVEL, "HS_LEVEL" )
    addLabels(labelDict, AS_LEVEL, "AS_LEVEL" )
    addLabels(labelDict, BS_LEVEL, "BS_LEVEL" )
    addLabels(labelDict, MS_LEVEL, "MS_LEVEL" )
    addLabels(labelDict, PHD_LEVEL, "PHD_LEVEL" )    
    addLabels(labelDict, MS_PHD_LEVEL, "GRAD_LEVEL" )
    
    
    return labelDict
    
def createOntoDict():
    ontoDict = {}
    DE_LEVEL = ["HS_LEVEL", "AS_LEVEL","BS_LEVEL","MS_LEVEL","PHD_LEVEL", "GRAD_LEVEL"]
    addLabels(ontoDict, DE_LEVEL,"DE_LEVEL" )  
    return ontoDict
    
def createDegreeGrammar():
    labelDict = createLabelDict()
    labelDict = addMoreLabels(labelDict)
    ontoDict = createOntoDict()
    labeler = Labeler(labelDict,ontoDict)
    return labeler  
 
         
class LabelMatcher(TokenMatcher): 
    
    def __init__(self, tokens):
        TokenMatcher.__init__(self, tokens, catchfun=lambda x:x , outfun=lambda x: [ y[1] for y in x ])
        
    def getWord(self, item):
        return item[0]
