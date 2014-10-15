# -*- coding: utf-8 -*-
"""
Created on Sun Oct 05 13:40:34 2014

@author: dlmu__000
"""

from baseir import BaseIr
from baseir import loadResume
import irutils
from jobaly.db.dbclient import DbClient 
import math

K1 = 1.2
B  = 0.75

class KL(BaseIr):    
     
         
    def calculateScores(self,resume):
        resume_content = irutils.processText(resume) 
        resume_tokens =  self.tfgetter.getTokens(resume_content)
        resumetf = self.tfgetter.getTf(resume_tokens) 
        resume_len = len(resume_tokens)
        resume_pq = {}
        for key in resumetf.keys():
            resume_pq[key] = float(resumetf[key])/resume_len
        print "resume_pq=", resume_pq        
       
        for job in self.jobs:
             tf = job["tf"]
             score = 0
             for key in resumetf.keys():
                 if tf.has_key(key):
                     job_p =  float (tf[key]) / job["length"]
                #     print "job_p=", job_p
                     score += resume_pq[key] * math.log10 (resume_pq[key] / job_p  )  
             job["score"] = score
             
def main(): 
    #webJobInfoCollName: test_jobinfo
    resumepath = "..\\..\\..\\data\\test_resumes\\Darin-Densley_web.txt"
    resume = loadResume(resumepath)
    print resume

    dbClient = DbClient('localhost', 27017, "jobaly")  
    jobCollection = dbClient.getCollection("test_jobinfo")  
    kl = KL(jobCollection)
    jobs = kl.matchResume(resume)
    
    for job in jobs:
        print job["_id"], job["score"]
    
if __name__ == "__main__": 
    main()
