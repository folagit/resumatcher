# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 15:42:46 2014

@author: dlmu__000
"
"""
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient
from jobdescparser import JobDescParser, JobDesc
from nltk.tokenize import sent_tokenize, word_tokenize

def dumpToText(listObj, fileName, lam):
     with open(fileName, "w") as f:
         for item in listObj:              
             line = lam(item) + "\n"
         #    print line.encode("GBK", "ignore")
             f.write(line.encode('utf8'))
         
def dumpToJson(listObj, fileName):
     with open(fileName, "w") as f:
         json.dump(listObj, f)
     
def dumpTwo(listObj, fileName , lam):
    txtFileName = fileName+".txt"
    jsonFileName = fileName+".json"
    dumpToText(listObj, txtFileName , lam)
    dumpToJson(listObj, jsonFileName)
    
def getAllSentsInColl(collection):
    allSents = []
    for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = [ (  jobDesc._id, sent )  for sent in  jobDesc.listAllSentences() ]
        allSents.extend(sents)  
    return allSents    
    
def termMatching(allSents,term):
    
    matchingSents =[]
    for (jid, sent) in allSents:
        tokens = [ token.lower() for token in word_tokenize(sent)]
        if term in tokens : 
            matchingSents.append((jid, sent))
    return  matchingSents  
 
def testGetAllSents():
    
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     allSents =  getAllSentsInColl(newCol)  
    
     dumpTwo(allSents, "sents\web_dev_sents_2" , ( lambda x: x[0] + ":" + x[1] ) )     

def testTermMatching():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     allSents =  getAllSentsInColl(newCol) 
     
     term = "experience"
     matchingSents = termMatching(allSents,term)
     
     dumpTwo(matchingSents, "sents\\matching_"+ term , ( lambda x: x[0] + ":" + x[1] ) )     
    
    
def main(): 
   # testParseAll()
    testTermMatching()
    
if __name__ == "__main__": 
    main()   