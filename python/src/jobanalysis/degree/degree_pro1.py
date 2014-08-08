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
from data.jobsentence import JSentence
import re
import operator

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

def  beforeDegree():
    data_set_name = "degree_1"       
    data = datautils.loadJson(data_set_name)
    dict1 = {}
    for item in data:
        words = item[1].lower().split()
        i = findToken("degree", words)
        if ( i != -1 ) :
            if i == 0 :
                term = "__NO__"
            else: 
                term = words[i-1]
      #  print term.encode("GBK", "ignore")
        if dict1.has_key(term):
            dict1[term]+=1
        else :
            dict1[term]=1
      #  print term.encode("GBK", "ignore")
    datautils.printStatDict(dict1)
    
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
    addLabels(labelDict, HS_LEVEL, "DE_LEVEL" )
    addLabels(labelDict, AS_LEVEL, "DE_LEVEL" )
    addLabels(labelDict, BS_LEVEL, "DE_LEVEL" )
    addLabels(labelDict, MS_LEVEL, "DE_LEVEL" )
    addLabels(labelDict, PHD_LEVEL, "DE_LEVEL" )    
    addLabels(labelDict, MS_PHD_LEVEL, "MS_PHD_LEVEL" )
    
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
    addLabels(labelDict, MAJOR_WEAK, "MAJOR_WEAK" )
    addLabels(labelDict, HIGHER_JJ, "HIGHER_JJ" )
    addLabels(labelDict, MD, "MD" )
    addLabels(labelDict, QUALIFICATION, "QUALIFICATION" )
    addLabels(labelDict, APPLICANT, "APPLICANT" )
    
       
  #  print labelDict
    return labelDict
    
def createDegreeGrammar():
    labelDict = setupLabelDict()
    labelGrammer = LabelGrammer(labelDict)
    return labelGrammer
 #   for item in labelGrammer.multiLabelList :
 #       print item
        
 #   for item in labelGrammer.labelTuples :
 #        print item
def printLabelGrammar(labelGrammer) :        
    for item in labelGrammer.labelTuples :
         print item
    
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
  #  printLabelGrammar(labelGrammer)
    degreeSent = JSentence(sent06.split())
    labelGrammer.labelSentence(degreeSent)
    degreeSent.printSentenct()  
   
    
def labelDegreeSet(data_set_name, outfileName):
    labelGrammer =  createDegreeGrammar()        
    data = datautils.loadJson(data_set_name)
     
    f = open(outfileName, "w")
    for item in data:
    #    print item
        words = item[2].split()
        degreeSent = JSentence(words)
        labelGrammer.labelSentence(degreeSent)
       
        print item[0]
        f.write (  item[0] + "\n\n") 
        
        table = degreeSent.printSentenct()  
   #     print table.get_string() + "\n\n"
        f.write( table.get_string()  + "\n\n" )        
        
def pipeLine():    
    data_set_name = "matching_degree_1"       
    data = datautils.loadJson(data_set_name)
   # preProcess(data)        
  

def test_removeSplash():
    line = "dfas feed dfe/df eed and/or de/iri "
    print removeSplash(line)
  
def main(): 
 #  createDegreeGrammar()
 #  beforeDegree()
 #   labelDegree()
 #   preProcess()
  #  labelDegreeSet()
 #  test_removeSplash()   
   
 #   data_set_name = "matching_degree_1"  
 #   target_set_name = "degree_1"     
        
   data_set_name = "matching_muldegree_3"  
   target_set_name = "degree_3"
   outfileName = "degree_3_label.txt"
   preProcess(data_set_name, target_set_name)
   labelDegreeSet(target_set_name,outfileName) 
    
if __name__ == "__main__": 
    main() 