# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 12:39:04 2014

@author: dlmu__000
"""

import re
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from nltk.tokenize import sent_tokenize, word_tokenize
from jobdescparser import JobDescParser, JobDesc
from jobaly.db.dbclient import DbClient
from degree import degreeparser
from jobaly.ontology.ontologylib import OntologyLib
from skill.skillparser import SkillParser
from model.resumemodel import ResumeModel
from pattern.en import tokenize   
from titles.titleprocess import preProcessTitle
from titles.titleprocess import getTitleModel


dev_roles=["intern", "internship", "engineer","architect", "developer",
           "programmer", "programmer"]

consultant_roles = ["consultant"]

scientist_roles = ["scientist" ]

other_roles = ["lead", "analyst",  "specialist" ]
 
roles = []
roles.extend(dev_roles)
roles.extend(consultant_roles)
roles.extend(scientist_roles)
roles.extend(other_roles)

def splitSentences(text):
  #  print "text=", text
    lines =   text.split("   ") 
  #  print "lines=",lines
  #  print "   -----------------  "
    return lines

skillParser = SkillParser()

def replaceCode(line):
  #  print "line ===", line 
    line =  re.sub (ur"\u2022|\u00b7|\uf09f|\uf0a7|\u0080|\u0099|\u00a2|\u0095|\u00d8|\u00bf|\u00c2|\u2219|\u20ac|\u2122", "",line)
    line =  re.sub ("·", "",line, re.UNICODE) 
    line =  re.sub (ur"\u2013", "-", line)
    line =  re.sub ("\*", "",line)
    line =  re.sub(ur"\u2019|\u2018|\u00e2|\u0092|\u2020" , "\'", line)
    line =  re.sub(ur"\u00ae", "", line)
    line =  re.sub(ur"\&", "and", line)
    
    line = line.strip()
    if line.find("-")==0 or line.find("\"")==0  \
        or line.find("\'")==0  or line.find("\,")==0  :
        line = line[1:].strip()
    
    return line
    
def removeSplash(line):
    slash_list = ["and/or", "PL/SQL"]  
    
    replace = True
    while replace:
        replace = False
        for word in line.split(): 
            if word.find("/") != -1 and len(word)>1:
                if  not ( word in slash_list ): 
               #     print "*****removeSplash phrase is: ",  word                            
                    newword = re.sub("/", " / ", word)
              #      print "newword=", newword
                    line = line.replace(word, newword) 
                    replace = True
   
    return line
   
def degreeWordReplace(line):
    line =  re.sub(ur"[B|b]achelor's", "bachelors", line)
    line =  re.sub(ur"[B|b]achelor \'s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \'s", "masters", line)
    line =  re.sub(ur"[B|b]achelor \' s", "bachelors", line)
    line =  re.sub(ur"[B|b]achelor s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \' s", "masters", line)    
    line =  re.sub(ur"[A|a]ssociate \' s", "associates", line)
    
    return line
   
def processLine(line):
    line = replaceCode(line)
    line = removeSplash(line)
    line = degreeWordReplace(line)

    return line    

def preprocess( sents ) :
    sents2 = []
    for line in sents:     
        newline = processLine(line)
    #    print "newline==" , newline
        sents2.append(  newline )
    
    return sents2
    
def processSents(resumeModel,  sents ):  
    for sent in sents:
    #    print "sent==" , sent
        if isDegreeSent(sent):
    #        print "degree = ",  sent
            parseDegree(resumeModel, sent )
        if isSkillSent(sent):
      #      print "skill = ",  sent
            parseSkill(resumeModel, sent )
            
        if isJobTitleSent(sent):
           #  print "title sent ==", sent
             parseTitle(resumeModel, sent )
            
    return resumeModel 

def termsMatching(terms, sent):

  #  print sent.encode("GBK", "ignore")
    tokens = [ token.lower() for token in word_tokenize(sent)]
    for term in  terms:      
        if term in tokens : 
            return True
    return False

def isDegreeSent(sent):    
     terms = ["degree", "B.A.", "PhD", "B.S.", "M.S." , "BA" ,"BS", "MS", "bachelor", "master", "phd","master's"]
     return termsMatching(terms, sent)       

def isSkillSent(sent):    
    return skillParser.isSkillSent(sent)   
    
def isJobTitleSent(sent):
    
    words = word_tokenize(sent.lower())
    lw = len(words)
  #  print "lw=", lw
   
    if lw < 6:
        for token in roles: 
            if token in words:
                print sent
                return True
                
    return False

def parseDegree(jobModel, sent ):
    degreeparser.parseDegreeSent(jobModel, sent )
       
def parseSkill(jobModel, sent ):
    skillParser.parseSkill(jobModel, sent)    

def parseTitle(resumeModel, sent ):
  #  print "title=", sent
    title = preProcessTitle(sent)
    titleModel = getTitleModel( title )
    resumeModel.titleModels.append(titleModel)
    

def getResumeSents(content):
  #  print "resume content=", content
    newlines = []
    content = content.replace("<br>", "\n")
    lines = content.split("\n")
    for line in lines:
     #   print "line =" , line
        linelist = splitSentences(line)
        for newline in linelist:
            newline = newline.strip()
            if len(newline) > 0 :
                newlines.append(newline)           
  #  i = 0    
  #  for line in newlines:
  #      i += 1
  #      print i,  '>>' , line
                
    return newlines

def parseResumeText(content):
    resumeModel = ResumeModel()
    sents = getResumeSents(content)
    sents = preprocess(sents)    
    processSents(resumeModel,  sents )       
    return resumeModel

def parseResume(resume):  
    if resume.has_key("_id") :
        resumeModel = ResumeModel(str(resume["_id"]))
    else :
        resumeModel = ResumeModel()
    sents = getResumeSents(resume["text"])
    sents = preprocess(sents)    
    processSents(resumeModel,  sents )       
    return resumeModel

def processResumes():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     resumeCollName = "web_resumes"
     
     resumemodelCollName = resumeCollName+"_model"
     resumeColl = srcBbClient.getCollection(resumeCollName)
     modelColl = srcBbClient.getCollection(resumemodelCollName)
   #  newCol = srcBbClient.getCollection("daily_job_info_2014-06-16")
      
   #  for resume in collection.find():   
     resume = resumeColl.find_one()  
     resumeModel = parseResume(resume)   
  #   modelColl.save(resumeModel.serialize())
     
     saveResumeModels(resumeColl, modelColl)
    
def saveResumeModels(resumeColl, modelColl):
     for resume in resumeColl.find():    
         print "--------id=", resume["_id"]
         resumeModel = parseResume(resume)   
         modelColl.save(resumeModel.serialize())

def processReusmeText(txtfile):
     with open(txtfile, 'r') as resume_file:
        resume = resume_file.read()
        resumeModel = parseResumeText(resume)  
    
def main(): 
  #   processResumes()
    resumefile = "resumes\\java.txt"
  #  resumefile = "resumes\\test1.txt"
    processReusmeText(resumefile)
     
if __name__ == "__main__": 
    main() 
