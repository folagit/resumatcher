# -*- coding: utf-8 -*-
"""
Created on Sun Aug 31 22:49:28 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from jobaly.db.dbclient import DbClient
from jobaly.ontology.ontologylib import OntologyLib
from jobdescparser import JobDescParser
from nltk.tokenize import word_tokenize
from data.datautils import dumpTwo


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
 
def getSentenceByTerm(collection, term, outputPath):
    
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
     dumpTwo(sortedsents, outputPath , ( lambda x: x[0] + ":" + x[1] ) )     
  
  # term must be low case
def testGetSentenceByTerm(term):
    
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     collection = srcBbClient.getCollection("daily_job_webdev")
     
     outputPath = '..\skill\output\\' + term
     getSentenceByTerm(collection, term, outputPath)
     

def getSentsByOntology():
     owlfile = "..\..\jobaly\ontology\web_dev.owl"
     ontology = OntologyLib(owlfile)
     terms = [ " "+ x.lower() for x in ontology.getLabelList()]
     terms.extend([" "+x.lower() for x in ontology.getAllClassNames()])
     
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")
     
     collection = newCol
     
     matchingSents = []
     for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
        jid = job["_id"]
        for sent in sents:
            c = 0
            sent = sent.lower()
            for term in terms:                
                if sent.find(term) != -1:
                   c+=1
                if c==3 : 
                    print sent.encode("GBK", "ignore")
                    matchingSents.append((jid, sent))
                    break
              
     sortedsents = sorted(matchingSents, key=lambda x:   len(x[1]) )
     dumpTwo(sortedsents, "..\skill\output\term" , ( lambda x: x[0] + ":" + x[1] ) )     
    
     
def main(): 
 #   getJavaScipt()
  #  testGetSentenceByTerm("hadoop")
    getSentsByOntology()
    
if __name__ == "__main__": 
    main()   