# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 22:42:06 2014

@author: dlmu__000
"""
from baseir import BaseIr
from tfgetter import TfGetter
import irutils
from jobaly.db.dbclient import DbClient 
import math

K1 = 1.2
B  = 0.75

class Okapi(BaseIr):
    
    def __init__(self, jobCollection):
         self.tfgetter =  TfGetter()   
         self.jobCollection = jobCollection
         self.processColl(self.jobCollection)    
         
    def processColl(self, jobcoll ):     
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
         
    def calculateScores(self,resume):
        resume_content = irutils.processText(resume) 
        resume_tokens =  self.tfgetter.getTokens(resume_content)
        idfdict = {}
        
        for token in resume_tokens:                        
            idfdict[token] = 0
            tokenNum = 0
            for job in self.jobs:
                 tf = job["tf"]
                 if tf.has_key(token):
                     tokenNum+=1
            idfdict[token] = math.log10( ( self.doc_num - tokenNum + 0.5 ) / (tokenNum + 0.5)  )
        
        for job in self.jobs:
             tf = job["tf"]
             score = 0
             for token in resume_tokens:
                 if tf.has_key(token):
                     n1 = tf[token] * (K1+1)
                     n2 = tf[token] +  K1*(1-B + B * job["length"] / self.avgLength )
                     score += idfdict[token] * (n1 / n2) 
             job["score"] = score

def main(): 
    #webJobInfoCollName: test_jobinfo

    dbClient = DbClient('localhost', 27017, "jobaly")  
    jobCollection = dbClient.getCollection("test_jobinfo")  
    okpai = Okapi(jobCollection)
    resume = "I a am good java programmer, PHP, XML, hope juse c++, skill" 
    jobs = okpai.matchResume(resume)
    
    for job in jobs:
        print job["_id"], job["score"]
    
if __name__ == "__main__": 
    main()
