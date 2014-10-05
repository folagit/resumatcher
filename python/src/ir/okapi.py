# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 22:42:06 2014

@author: dlmu__000
"""
from baseir import BaseIr
from tfgetter import TfGetter
import irutils
from jobaly.db.dbclient import DbClient 


K1 = 1.2
B  = 0.75

class Okapi(BaseIr):
    
    def __init__(self, jobCollection):
         self.tfgetter =  TfGetter()   
         self.jobCollection = jobCollection
         self.processColl(self.jobCollection)    
         
    def getJobTfIdf(self, jobcoll ):     
         self.jobs = []        
         self.doc_num = 0
         sum_length = 0
         for item in jobcoll.find(): 
             content = irutils.processText(item["summary"])    
             tokens =  self.tfgetter.getTokens(content)
             tf = self.tfgetter.getTf(content)          
             item['tf'] =  tf
             item['length'] = len(tokens)
             self.jobs.append(item)
             self.doc_num+=1
             sum_length += item['length']
         self.avgLength = sum_length/self.doc_num

def main(): 
    #webJobInfoCollName: test_jobinfo

    dbClient = DbClient('localhost', 27017, "jobaly")  
    jobCollection = dbClient.getCollection("test_jobinfo")  
    tfIdfMatch = Okapi(jobCollection)
    resume = "I a am good java programmer, PHP, XML, hope juse c++, skill" 
    jobs = tfIdfMatch.matchResume(resume)
    
    for job in jobs:
        print job["_id"], job["score"]
    
if __name__ == "__main__": 
    main()
