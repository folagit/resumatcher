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
from degree import degreeparser
from jobaly.ontology.ontologylib import OntologyLib
from skill.skillparser import SkillParser
from model.jobmodel import JobModel
from titles.titleprocess import processTitle   
from preprocess import replaceCode

skillParser = SkillParser()


    
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
    sents = jobDesc.listAllSentences() 
    sents2 = []
    for line in sents:     
        sents2.append( processLine(line)  )
    
    return sents2
    
def processSents(jobModel,  sents ):       
     
    for sent in sents:
        if isDegreeSent(sent):
            parseDegree(jobModel, sent )
        if isSkillSent(sent):
            parseSkill(jobModel, sent )
            
    return jobModel 

def termsMatching(terms, sent):

  #  print sent.encode("GBK", "ignore")
    tokens = [ token.lower() for token in word_tokenize(sent)]
    for term in  terms:      
        if term in tokens : 
            return True
    return False

def isDegreeSent(sent):    
     terms = ["degree", "B.S.", "M.S." ,"BS", "MS", "bachelor", "master", "phd","master's"]
     return termsMatching(terms, sent)       

def isSkillSent(sent):    
    return skillParser.isSkillSent(sent)   

def parseDegree(jobModel, sent ):
    degreeparser.parseDegreeSent(jobModel, sent )
       
def parseSkill(jobModel, sent ):
    skillParser.parseSkill(jobModel, sent)    

 

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub(' ', text)

def removeHtml(coll):    
     for job in coll.find():
         content = remove_tags(job["summary"]).strip()
         job["notag"] = content
         coll.save(job)

def processjobs(dbname, collname):
     srcBbClient = DbClient('localhost', 27017, dbname)
     jobCollName = collname
     
     jobmodelCollName = jobCollName+"_model"
     collection = srcBbClient.getCollection(jobCollName)
     modelColl = srcBbClient.getCollection(jobmodelCollName)
   #  newCol = srcBbClient.getCollection("daily_job_info_2014-06-16")
      
     for job in collection.find():       
         sents = preprocess(job)
         jobModel = JobModel(job["_id"])       
         processSents(jobModel,  sents )
         
         titleModel = processTitle(job)
         jobModel.titleModel = titleModel
         modelColl.save(jobModel.serialize())
         
     
def main(): 
     processjobs()
     
if __name__ == "__main__": 
    main() 