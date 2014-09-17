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
from jobaly.match.matchercompiler  import MatcherCompiler

from  data import datautils

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
    
    addDegreeLabel(labelDict)
    addMajorLabels(labelDict)
    addOtherLabels(labelDict)
    
    return labelDict
    
def addDegreeLabel(labelDict):
    DEGREE = ["degree","degrees"]
    HS_LEVEL = ["High School Diploma", "High School" ,"GED", "general Educational Development" , "General Educational Degree"]    
    AS_LEVEL = ["AS","Associate","Associates", "AA", "A.A."]
    BS_LEVEL = ["Baccalaureate","bachelors", "bachelor" ,"B.S.", "B.S","BS","BA","BA/BS", "BABS", "BSBA", "B.A." ,"4-year","4-year", "4 year", "four year","college","Undergraduate" , "University" ]    
    MS_LEVEL = ["masters", "MS", "M.S.", "master", "MA" , "MSc"]
    PHD_LEVEL = ["PhD", "Ph.D", "doctorate" ]
    MS_PHD_LEVEL = ["Graduate", "advanced" ]
    DEGREE_JJ = [ "similar", "related","Relevant", "equivalent","based" ]
    
    addLabels(labelDict, DEGREE, "DEGREE" )  
    addLabels(labelDict, DEGREE_JJ, "DEGREE_JJ" )
    addLabels(labelDict, HS_LEVEL, "HS_LEVEL" )
    addLabels(labelDict, AS_LEVEL, "AS_LEVEL" )
    addLabels(labelDict, BS_LEVEL, "BS_LEVEL" )
    addLabels(labelDict, MS_LEVEL, "MS_LEVEL" )
    addLabels(labelDict, PHD_LEVEL, "PHD_LEVEL" )    
    addLabels(labelDict, MS_PHD_LEVEL, "GRAD_LEVEL" )   
   
def addMajorLabels(labelDict):      
   
    MAJOR_OTHERS = [ "biological sciences", "Physics",  "chemistry" ,  "Technology Management" , \
                     "Marketing", "Business", "Finance" , "Economics", "accounting", \
                     "Communications", "Communication Sciences",  "Journalism", "Geoscience", \
                     "transportation engineering","Anthropology","Sociology" ,"Behavioral Science", \
                     "Fine Arts", "Behavioral Sciences", "nursing"]
   
    MAJOR_GENERAL = ["engineering", "science", "numerical", "Management", "Art", "design", "technical" , "Technology" ]
    
    MAJOR_CS = ["computer science", "Comp Sci", "CompSci" , "computer","computer sciences" , "CS", "Computing Science " ,\
                  "computer programming" , "programming", "Software Engineering", "Artificial Intelligence","SE" ]
    MAJOR_CE = ["CE" , "computer engineering", ]
    MAJOR_EE = ["EE", "signal processing", "Electrical Engineering ", "Telecom" , "Electronic Engineering"]
    MAJOR_MATH = ["Applied Mathematics", "mathematics", "math" , ]    
    MAJOR_STAT = ["statistics","biostatistics" ]    
    MAJOR_INFO = [ "IS",  "Information Systems",  "Digital Media", "Information Technology", \
                   "Web Development", "Information Sciences","MIS", "CIS", \
                   "Computer Information Systems",  "GIS" , "IT", "Information Science" ]
    
    MAJOR_DESIGN= ["Web Design", "Interactive Design","Graphic Design", "Human-Computer Interaction" , "Visual Arts" , "photography"]    
    MAJOR_RELATED = ["related field" , "related discipline", "related area", "related fields", \
                     "relevant discipline" , "related subject", "relevant subject", \
                     "a related field" , "a related discipline", "a related area",  \
                     "a relevant discipline" , "a related subject", "a relevant subject" ,\
                     "a similar discipline"]
    
    addLabels(labelDict, MAJOR_OTHERS, "MAJOR_OTHERS" )
    addLabels(labelDict, MAJOR_GENERAL, "MAJOR_GENERAL" )    
    addLabels(labelDict, MAJOR_CS, "MAJOR_CS" ) 
    addLabels(labelDict, MAJOR_CE, "MAJOR_CE" )  
    addLabels(labelDict, MAJOR_EE, "MAJOR_EE" )  
    addLabels(labelDict, MAJOR_MATH, "MAJOR_MATH" )  
    addLabels(labelDict, MAJOR_STAT, "MAJOR_STAT" )  
    addLabels(labelDict, MAJOR_INFO, "MAJOR_INFO" )  
    addLabels(labelDict, MAJOR_DESIGN, "MAJOR_DESIGN" )  
    addLabels(labelDict, MAJOR_RELATED, "MAJOR_RELATED" )  
    
    
def addOtherLabels(labelDict):
    MAJOR_DEGREE = ["MBA", "BSCS", "BSEE", "MSCS", "MSEE", "MSCE","MPH" ]
    addLabels(labelDict, MAJOR_DEGREE, "MAJOR_DEGREE" )
    
    PREFER_RB = ["preferably"]  
    PREFER_NN = [ "a plus", "at least","minimum" ]
    PREFER_VBD = ["preferred", "required","desired" ]    
    PREFER_JJ = [ "a plus",  "mandatory","desirable"]    
    PREFER_VB =  ["Requires" , "have", "Pursuing", "Prefer"]
    MD = ["must", "should","would"]
    HIGHER_JJ = ["above", "higher","greater","better"]
    
    EXPERIENCE = ["experience" , "work experience" , "practical experience" ,"professional experience" ]
    EDUCATION = ["education"]
    
    QUALIFICATION = ["Qualifications", "Qualification"]
    APPLICANT = [ "Applicant" ,"Applicants" ,"candidate"]
    
    addLabels(labelDict, PREFER_RB, "PREFER_RB" )
    addLabels(labelDict, PREFER_NN, "PREFER_NN" )
    addLabels(labelDict, PREFER_VBD, "PREFER_VBD" )
    addLabels(labelDict, PREFER_JJ, "PREFER_JJ" )
    addLabels(labelDict, PREFER_VB, "PREFER_VB" )
  
    addLabels(labelDict, HIGHER_JJ, "HIGHER_JJ" )
    addLabels(labelDict, MD, "MD" )
    addLabels(labelDict, QUALIFICATION, "QUALIFICATION" )
    addLabels(labelDict, APPLICANT, "APPLICANT" )   
    addLabels(labelDict, EXPERIENCE, "EXPERIENCE" )
    addLabels(labelDict, EDUCATION, "EDUCATION" )
    
    
def createOntoDict():
    ontoDict = {}
    DE_LEVEL = ["HS_LEVEL", "AS_LEVEL","BS_LEVEL","MS_LEVEL","PHD_LEVEL", "GRAD_LEVEL"]
    MAJOR = [ "MAJOR_OTHERS" , "MAJOR_GENERAL", "MAJOR_CS", "MAJOR_CE",  "MAJOR_RELATED" ,
              "MAJOR_EE", "MAJOR_MATH",  "MAJOR_STAT",  "MAJOR_INFO" ,    "MAJOR_DESIGN" ]
    addLabels(ontoDict, DE_LEVEL,"DE_LEVEL" )  
    addLabels(ontoDict, MAJOR, "MAJOR" ) 
    return ontoDict
    
def createDegreeLabeler():
    labelDict = createLabelDict()   
    ontoDict = createOntoDict()
    labeler = Labeler(labelDict,ontoDict)
    return labeler  

def labelSent(labeler, matcher, sent):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    i = matcher.findMatching(labeledArray) 
    return i, degreeSent   
         
class LabelMatcher(TokenMatcher): 
    
    def __init__(self, tokens):
        TokenMatcher.__init__(self, tokens, catchfun=lambda x:[ y[1] for y in x ] , outfun=lambda x: x )
        
    def getWord(self, item):
        return item[0]
        
class UnitLabelMatcher(UnitTokenMatcher): 
    
    def __init__(self, token):
        UnitTokenMatcher.__init__(self, token, catchfun=lambda x:[ y[1] for y in x ]  , outfun=lambda x: x )
        
    def getWord(self, item):
        return item[0]
        
       
        
class OriTextMatcher(TokenMatcher): 
    
    def __init__(self, tokens):
        TokenMatcher.__init__(self, tokens, catchfun=lambda x:[ y[2][0] for y in x ] , outfun=lambda x: x )
    
    # so one unit can only has one word     
    def getWord(self, item):
        return item[2][0]
        
labeler =  createDegreeLabeler() 
def getOntoType(result):
 #   print "result=",result
    newresult = []
    for item in result:
     #   print " ^item=",item
        if item != [] and \
          labeler.ontoDict.has_key(item):
             newresult.append((labeler.ontoDict[item],item))
    return newresult

def labelSentByMatchers(matchers, sent):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
#    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    matcher =  matchSent(matchers, labeledArray)
    return degreeSent, matcher

def matchSent(matchers, labeledArray):
    
    for matcher in matchers:
        i = matcher.findMatching(labeledArray) 
        if i != -1:
            matcher.matchNum += 1
            return  matcher
            
    return  None
    

    
def labelDegreeSet(matchers, data_set_name, outfileName,failfilename):
   
    for matcher in matchers:       
            matcher.matchNum = 0     
     
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")
    f2 = open(failfilename, "w")
    total = 0
    m = 0
    for item in data:
    #    print item
        sent = item[2]    
        sid = item[0]         
        matcher = None
        degreeSent, matcher = labelSentByMatchers(matchers, sent) 
     
        if matcher is not None:
            output = matcher.output()
            found = matcher.found
        else:
            output = None
            found = None
        
        print sid ,found, output 
        total += 1
        if matcher is not None :
            m+=1
            f.write( sent +"\n\n" )
            f.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f.write( str(found) + "   " + str(output) +"\n\n" )
        else :
            f2.write( sent +"\n\n" )
            f2.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
             
    f2.write( "\n\n match="+ str( m) + "  total="+ str( total) + "  radio=" + str (float(m)/total) +"\n" )
             
    print "match=", m, "  total=", total, "  radio=", float(m)/total
    
    i = 0
    for matcher in matchers :
        i+=1
        print "matcher ", i, ":", matcher.matchNum
        f2.write( "\n matcher " + str( i) + ":" + str( matcher.matchNum ) )

matcherCompiler = MatcherCompiler(tokenMatcher=UnitLabelMatcher, defaultOutfun=getOntoType ,  debug=True) 