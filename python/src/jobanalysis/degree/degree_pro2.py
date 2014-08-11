# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 20:31:27 2014

@author: dlmu__000

"""
import sys
sys.path.append("..")
from  data import datautils
from data.tokenfilter import *
from data.labelgrammer import LabelGrammer
from data.jobsentence import JobSentence
import re
import operator

sys.path.append("../..")
from jobaly.fst.tokenre  import *
from jobaly.match.matcher  import *

def removeSplash(line):
    slash_list = ["and/or", "PL/SQL"]  
    
    replace = True
    while replace:
        replace = False
        for word in line.split(): 
            if word.find("/") != -1 and len(word)>1:
                if  not ( word in slash_list ): 
                    print "*****removeSplash phrase is: ",  word                            
                    newword = re.sub("/", " / ", word)
                    line = re.sub(word, newword, line ) 
                    repalce = True
   
    return line

def preProcessFun(line):
    line =  re.sub (ur"\u2022|\u00b7|\uf09f|\uf0a7|\u0080|\u0099|\u00a2|\u0095|\u00d8|\u00bf|\u00c2|\u2219|\u20ac|\u2122", "",line)
    line =  re.sub ("·", "",line, re.UNICODE) 
    line = re.sub (ur"\u2013", "-", line)
    line =  re.sub ("\*", "",line)
    line =  re.sub(ur"\u2019|\u2018|\u00e2|\u0092|\u2020" , "\'", line)
    line = re.sub(ur"\u00ae", "", line)
    line =  re.sub(ur"\&", "and", line)
    
    
    
    if line.find("/") != -1 :
         line = removeSplash(line)  

    line =  re.sub(ur"[B|b]achelor's", "bachelors", line)
    line =  re.sub(ur"[B|b]achelor \'s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \'s", "masters", line)
    line =  re.sub(ur"[B|b]achelor \' s", "bachelors", line)
    line =  re.sub(ur"[B|b]achelor s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \' s", "masters", line)    
    line =  re.sub(ur"[A|a]ssociate \' s", "associates", line)      
   
    line = line.strip()
    if line.find("-")==0 or line.find("\"")==0  \
        or line.find("\'")==0  or line.find("\,")==0  :
        line = line[1:].strip()
    return line

dumpLam1 = lambda x: x[0] + " | " + x[1]
dumpLam2 = lambda x: x[0] + " | " + str( x[1] ) + " | " + x[2]

def preProcess(data_set_name, target_set_name):
    
    max_length = 200
    data = datautils.loadJson(data_set_name)    
    newdata = []
    for item in data:
        if len (item[1] ) < max_length : 
            item.append ( preProcessFun(item[1]) )
            item[1] = len(item[2].split())
            newdata.append(item)
    newdata = sorted(newdata, key=operator.itemgetter(1) )
    datautils.dumpTwo(newdata, target_set_name, dumpLam2)    

def addLabels(labelDict, items, label):
    for item in items:
        labelDict[item] = label
   
def setupLabelDict():
      
    labelDict = {  "or": "OR", "OR": "OR", "and" : "AND" ,  "in": "IN" , "In":"IN" , \
           "of" : "OF", "and/or" : "AND_OR", "from" :"FROM" , "with":"WITH" , \
           "at":"AT" ,"about":"ABOUT" , "for" : "FOR" ,"as":"AS" }
    BE = ["Be","be", "is", "are", "was", "were", "am"]    
    DT = ["a", "A", "an", "An", "The", "the"]  
    DIGIT = ['one', "two", "three", "four", "five", "seven", "eight", "night", "ten" ]
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
    YEAR = ["year", "years", "yr"]
    QUALIFICATION = ["Qualifications", "Qualification"]
    APPLICANT = [ "Applicant" ,"Applicants" ,"candidate"]
    
    addLabels(labelDict, BE, "BE" )  
    addLabels(labelDict, DT, "DT" )  
    addLabels(labelDict, DIGIT, "DIGIT" )  
    addLabels(labelDict, DEGREE, "DEGREE" )    
    
    addLabels(labelDict, MAJOR, "MAJOR" )
    addLabels(labelDict, MAJOR_DEGREE, "MAJOR_DE" )
    
    addLabels(labelDict, EXPERIENCE, "EXPERIENCE" )
    addLabels(labelDict, EDUCATION, "EDUCATION" )
    addLabels(labelDict, YEAR, "YEAR" )
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
    
    degreeDict = {}
    addLabels(degreeDict, HS_LEVEL, "HS_LEVEL" )
    addLabels(degreeDict, AS_LEVEL, "AS_LEVEL" )
    addLabels(degreeDict, BS_LEVEL, "BS_LEVEL" )
    addLabels(degreeDict, MS_LEVEL, "MS_LEVEL" )
    addLabels(degreeDict, PHD_LEVEL, "PHD_LEVEL" )    
    addLabels(degreeDict, MS_PHD_LEVEL, "GRAD_LEVEL" )
    
    global degreeDict
    
  #  print labelDict
    return labelDict
    
def createOntoDict():
    ontoDict = {}
    DE_LEVEL = ["HS_LEVEL", "AS_LEVEL","BS_LEVEL","MS_LEVEL","PHD_LEVEL", "GRAD_LEVEL"]
    addLabels(ontoDict, DE_LEVEL,"DE_LEVEL" )  
    return ontoDict
    
def createDegreeGrammar():
    labelDict = setupLabelDict()
    ontoDict = createOntoDict()
    labelGrammer = LabelGrammer(labelDict,ontoDict)
    return labelGrammer
 #   for item in labelGrammer.multiLabelList :
 #       print item
        
 #   for item in labelGrammer.labelTuples :
 #        print item
def printLabelGrammar(labelGrammer) :        
    for item in labelGrammer.labelTuples :
         print item
         
class LabelMatcher(TokenMatcher): 
        
    def getWord(self, item):
        return item[0]
    
    def output(self):             
        return  self.catch[0][1]  
        
    
def labelDegree():

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
            if labelGrammer.ontoDict.has_key(item):
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
    
    
  #  printLabelGrammar(labelGrammer)
    degreeSent = JobSentence(sent02.split())
    labelGrammer.labelSentence(degreeSent)
    print degreeSent.printSentenct()  
    labeledArray = degreeSent.getLabeledArray(labelGrammer.ontoDict)
    print degreeSent.printLabeledArray()
        
    
    runmatcher = degreeSeq2
 #   i = matcher3.findMatching(labeledArray)     
    i = runmatcher.findMatching(labeledArray)     
    print "matching at:", i 
    print "extraction result is:", runmatcher.output()
  
def main(): 
 #  createDegreeGrammar()
 #  beforeDegree()
 #   labelDegree()
 #   preProcess()
  #  labelDegreeSet()
 #  test_removeSplash()   
        
   data_set_name = "matching_muldegree_3"  
   target_set_name = "degree_3"
   outfileName = "degree_3_label.txt"
   
   data_set_name = "output\\matching_degree_1"  
   target_set_name = "output\\degree_1" 
   outfileName = "output\\degree_1_label.txt"
   outfileName = "output\\degree_1_layer1.txt"
   
   preProcess(data_set_name, target_set_name)
#   labelDegreeSet(target_set_name,outfileName) 
   getLabeledSentence(target_set_name,outfileName) 
if __name__ == "__main__": 
    labelDegree() 