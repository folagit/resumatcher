# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 22:49:28 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from jobaly.db.dbclient import DbClient
from jobdescparser import JobDescParser
from nltk.tokenize import word_tokenize
from data.datautils import dumpTwo

def processColl(collection):
    allSents.extend(sents)  
    
def getJavaScipt(): 
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")
     
     collection = newCol
     term = "javascript"
     matchingSents = []
     for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
        jid = job["_id"]
        for sent in sents:
            tokens = [ token.lower() for token in word_tokenize(sent)]              
            if term in tokens : 
                matchingSents.append((jid, sent))
                print sent.encode("GBK", "ignore")
                
     sortedsents = sorted(matchingSents, key=lambda x:   len(x[1]) )
     dumpTwo(sortedsents, "..\skill\output\javascript" , ( lambda x: x[0] + ":" + x[1] ) )     
  
     
def main(): 
    getJavaScipt()
    
if __name__ == "__main__": 
    main()   