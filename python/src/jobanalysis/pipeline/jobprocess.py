# -*- coding: utf-8 -*-
"""
Created on Fri Sep 05 00:03:18 2014

@author: dlmu__000
"""

import re


import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from nltk.tokenize import sent_tokenize, word_tokenize
from jobdescparser import JobDescParser, JobDesc
from jobaly.db.dbclient import DbClient

def replaceCode(line):
    line =  re.sub (ur"\u2022|\u00b7|\uf09f|\uf0a7|\u0080|\u0099|\u00a2|\u0095|\u00d8|\u00bf|\u00c2|\u2219|\u20ac|\u2122", "",line)
    line =  re.sub ("·", "",line, re.UNICODE) 
    line = re.sub (ur"\u2013", "-", line)
    line =  re.sub ("\*", "",line)
    line =  re.sub(ur"\u2019|\u2018|\u00e2|\u0092|\u2020" , "\'", line)
    line = re.sub(ur"\u00ae", "", line)
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
    

def preprocess( job ):
    jobDesc = JobDescParser.parseJobDesc(job)
    jobid = jobDesc._id
    sents = jobDesc.listAllSentences() 
  
    for line in sents:     
       processLine(line)  
    
    return sents
    
def processSents(jobModel,  sents ):       
     
    for sent in sents:
        if isDegreeSent(sent):
            parseDegree(jobModel, sent )
        if isSkillSent(sent):
            parseSkill(jobModel, sent )
            
    return jobModel 

def termsMatching(terms, sent):

    print sent.encode("GBK", "ignore")
    tokens = [ token.lower() for token in word_tokenize(sent)]
    for term in  terms:      
        if term in tokens : 
            return True
    return False

def isDegreeSent(sent):    
     terms = ["degree", "B.S.", "M.S." ,"BS", "MS", "bachelor", "master", "phd","master's"]
     return termsMatching(terms, sent)       

def isSkillSent(sent):
    return False   

def parseDegree(jobModel, sent ):
    pass
       
def parseSkill(jobModel, sent ):
    pass    

def processTitle(jobModel, sent ):
    pass    

def processjobs():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     collection = srcBbClient.getCollection("daily_job_webdev")
   #  newCol = srcBbClient.getCollection("daily_job_info_2014-06-16")
      
     for job in collection.find(): 
         sents = preprocess(job)
         jobModel = []
         processSents(jobModel,  sents )
         
   
     
def main(): 
     processjobs()
     
if __name__ == "__main__": 
    main() 