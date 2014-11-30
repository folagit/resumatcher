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
    #    print "resume_len=" ,resume_len        
    #    print "resume_pq=", resume_pq        
       
        for job in self.jobs:
             tf = job["tf"]
             job_len = job["length"]
        #     print "job_len=", job_len
             score = 0
             for key in resumetf.keys():
                 if tf.has_key(key):
                     job_p =  float (tf[key]) / job_len 
                #     print "job_p=", job_p
                     score += job_p * math.log (   job_p / resume_pq[key] )  
             job["score"] = score
             
def main(): 
    #webJobInfoCollName: test_jobinfo
    resume =  loadResume("..\\..\\..\\data\\test_resumes\\Darin-Densley_web.txt")
  #  resume =  loadResume("..\\..\\..\\data\\test_resumes\\Java-Developer.txt")
  #  resume =  loadResume("..\\..\\..\\data\\test_resumes\\Fong-Kuo_data.txt")

  #  print resume
  #  resume = "I a am good java programmer, PHP, XML, hope juse c++, skill" 
    dbClient = DbClient('localhost', 27017, "jobaly")  
    jobCollection = dbClient.getCollection("job100")  
    kl = KL(jobCollection)
    jobs = kl.matchResume(resume)
    
    for job in jobs:
        print job["_id"], job["score"]
    
if __name__ == "__main__": 
    main()
