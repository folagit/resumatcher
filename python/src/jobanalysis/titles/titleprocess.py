# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 22:58:20 2014

@author: dlmu__000
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from jobaly.db.dbclient import DbClient
from data.jobsentence import JobSentence
from titlelabler import createTitleLabeler
from commonLabelfuns import matchSent
from commonLabelfuns import LabelMatcher
from nltk.tokenize import word_tokenize
from pipeline.preprocess import replaceCode

dev_roles=["Intern","Engineer","Architect","Development","Developer",
       "Programmer","dev","Computer Programmer","lead","CONSULTANT","Eng."]

common_dev_roles = [ "Engineer", "Development","Developer",
       "Programmer","dev","Computer Programmer", "Eng"]

pro_lang = ["java", "c++", "python", ".net", "javascript", 
            "PHP", "ruby", "c#", "Ruby on Rails", "SQL" ]

skill_set = ["jsp", "asp", "html", "css"]

dev_domain = ["web", "mobile", "UI" , "db", "cloud" , "database", "Middleware", "full stack"]    

dev_platform = ["ios", "android", "linux", "j2ee" ]

software = ["oracle", "sas"]

job_type = ["software" , "test" , "administrator","Analyst"]
 

def tokensIn(tokens, words, lower=True):
    for token in tokens:
        if  lower :
            token = token.lower()
        if token in words: 
            return token
     

def preProcessTitle(sent):
    sent = replaceCode(sent)
    sent = sent.replace("/"," ") 
    return sent

def getTitleModel(title ):
    model = {}
    words = word_tokenize(title.lower() )
    processRole(words, model)
    processLevel(words, model)
    processDomain(words, model)
    
    return model  
    
    
def processRole(words, model):
    role = tokensIn(common_dev_roles, words)
    if role is not None:
        model["role"] = "DEV"
        model["level"] = 3
  
# intern: 1, Jr.:2, Eng:3, Sr.:4, Lead:5, architect:6, CTO:7
def processLevel(words, model):
     
    if tokensIn(["intern"], words) is not None:
        model["level"] = 1
    
    if tokensIn(["jr.", "Junior"], words) is not None:
        model["level"] = 2
        
    if tokensIn(["sr.", "Senior"], words) is not None:
        model["level"] = 4
        
    if tokensIn([ "Lead" ], words) is not None:
        model["level"] = 5
        
    if tokensIn(["architect" ], words) is not None:
        model["level"] = 6
        
    if tokensIn(["cto" ], words) is not None:
        model["level"] = 7
        
    
def processDomain(words, model):
    domain = tokensIn(dev_domain, words)
    if domain is not None:
        model["domain"] = domain    

    lang = tokensIn(pro_lang, words)
    if lang is not None:
        model["pro_lang"] = lang  
        
    platform = tokensIn(dev_platform, words)
    if platform is not None:
        model["platform"] = platform  
 
def processTitle(job):
    sid = job["_id"]        
    title = job["jobtitle"]
    title = preProcessTitle(title)
    titleModel = getTitleModel( title )
    print sid ,  "---->>>" , title
    print titleModel    
    
    return  titleModel        

def processTitles(dbname, collname):
     srcBbClient = DbClient('localhost', 27017, dbname)
     jobCollName = collname
     collection = srcBbClient.getCollection(jobCollName)      
     for job in collection.find(): 
        titleModel = processTitle(job)        
 
     
def main(): 
    targetDb = "jobaly"
    targetCollName = "job1000" 
    processTitles( targetDb, targetCollName )
     
if __name__ == "__main__": 
    main() 