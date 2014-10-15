import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from tfidf_getter import *
import math
import irutils

def loadResume(filepath):
    with open (filepath, "r") as myfile:
        data=myfile.read().replace('\n', '')
        return data

def getQueryWtfIdf(wtf,idf):
    wtfidf = {} 
    sumweight = 0
    for key, value in wtf.iteritems():   
        if idf.has_key(key):     
            wtfidf[key]=value*idf[key]
            sumweight += wtfidf[key] * wtfidf[key]
    length = math.sqrt(sumweight)
    return wtfidf, length
            
class TfIdfMatch():
    
    def __init__(self, jobCollection):
        self.tfIdfGetter = TfIdfGetter()
        self.jobCollection = jobCollection
        self.jobs_idf , self.jobs = self.tfIdfGetter.getJobTfIdf(self.jobCollection)
        
    def getResumeWight(self, resume):
        content = irutils.processText(resume)       
        tf = self.tfIdfGetter.getTf(content)
        wtf = getwtf(tf)
        wtfidf, length  = getQueryWtfIdf(wtf, self.jobs_idf)
        return wtfidf
    
    def getCosine(self, job, resume_wtfidf):
        sum_weight = 0
        job_wtfidf = job["wtfidf"]
        for key , value in resume_wtfidf.iteritems():
            if job_wtfidf.has_key(key):
                sum_weight += value * job_wtfidf[key]
     #           print key, value
                
        return sum_weight / job['length']
        
    def calculateScores(self,resume):
        resume_wtfidf = self.getResumeWight(resume)
        for job in self.jobs:
            score = self.getCosine(job, resume_wtfidf)
        #    print "score=",score
            job["score"] = score
        
    def matchResume(self, resume):
        self.calculateScores(resume)
        self.jobs.sort(key=lambda x: x["score"], reverse=True)
        return self.jobs    
        

def main(): 
    #webJobInfoCollName: test_jobinfo
    resumepath = ""
    resume =  loadResume("..\\..\\..\\data\\test_resumes\\Darin-Densley_web.txt")
    print resume
    dbClient = DbClient('localhost', 27017, "jobaly")  
    jobCollection = dbClient.getCollection("test_jobinfo")  
    tfIdfMatch = TfIdfMatch(jobCollection)
    
    jobs = tfIdfMatch.matchResume(resume)
    
    for job in jobs:
        print job["_id"], job["score"]
    
if __name__ == "__main__": 
    main()
