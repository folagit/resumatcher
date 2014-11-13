# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 22:58:20 2014

@author: dlmu__000
"""
import re
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from jobaly.db.dbclient import DbClient
from data.jobsentence import JobSentence
from titlelabler import createTitleLabeler
from commonLabelfuns import matchSent
from commonLabelfuns import LabelMatcher


matcher1 = LabelMatcher( "ROLE_PRE") + LabelMatcher( "ROLE_NAME")

labeler =  createTitleLabeler() 
matchers = [matcher1]

def processTitle(title):
    titleSent = JobSentence(title.lower().split())
    labeler.labelSentence(titleSent)    
    labeledArray = titleSent.getLabeledArray(labeler.ontoDict)
  #  print titleSent.printLabeledArray()    
    matcher =  matchSent(matchers, labeledArray)
    return  matcher

def processTitles(dbname, collname):
     srcBbClient = DbClient('localhost', 27017, dbname)
     jobCollName = collname
     collection = srcBbClient.getCollection(jobCollName)      
     for job in collection.find(): 
        sid = job["_id"]
        title = job["jobtitle"]
        matcher = processTitle(title)
        
        if matcher is not None:
            output = matcher.output()
            found = matcher.found
        else:
            output = None
            found = None
        
        print sid , title
        print   found, output 
   
     
def main(): 
    targetDb = "jobaly"
    targetCollName = "job100" 
    processTitles( targetDb, targetCollName )
     
if __name__ == "__main__": 
    main() 