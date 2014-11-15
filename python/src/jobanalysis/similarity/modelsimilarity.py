# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 17:26:04 2014

@author: dlmu__000
"""
import operator
import random
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from jobaly.db.dbclient import DbClient
from jobaly.ontology.ontologylib import OntologyLib
from jobaly.ontology import ontologylib
from model.jobmodel import JobModel
from model.resumemodel import ResumeModel
import pairdistance
from titles.titleprocess import titleSim


degreeDict = {"HS_LEVEL": 1,  "AS_LEVEL": 2,  "BS_LEVEL": 3, "MS_LEVEL": 4, "PHD_LEVEL": 5, "GRAD_LEVEL": 6 }
CS_RELATED=set(["MAJOR_EE", "MAJOR_INFO", "MAJOR_CE" ])


def transferDegree(degees):
    degeesList = list(degees)
    degreeNum = []
    for degree in degeesList:
        degreeNum.append(degreeDict[degree])
    degreeNum = sorted(degreeNum, reverse=True)    
    return degreeNum
  
class ModelSimilarity():
    
    def __init__(self):
        self.weightVector = [ 0.1, 0.1, 0.4, 0.4 ]
        self.weightVector = [ 0.05, 0.05, 0.4, 0.5 ]
        self.ontology = ontologylib.createOntology()
        self.pairDict = pairdistance.loadPairValues()

    def getSimilarity(self, resumeModel,  jobModel):
        simVector = [0] * 4
        simVector[0] = self.getDegreeSim(resumeModel,  jobModel)    
        simVector[1] = self.getMajorSim (resumeModel,  jobModel)  
        simVector[2] = self.getSkillSim (resumeModel,  jobModel)  
        simVector[3] = self.getTitleSim (resumeModel,  jobModel)  
        
        
        sumValue = 0
        for i in range(len(simVector)):
            sumValue += ( simVector[i] * self.weightVector[i] )
            
        return sumValue
        
    def getDegreeSim(self, resumeModel,  jobModel):
        resumeDegree = resumeModel.degrees
        jobDegree = jobModel.degrees     
         
        if len(jobDegree) == 0 :
            return 1
        
        if len(resumeDegree) == 0 : 
            return 0
        resumeNum = transferDegree(resumeDegree)
        jobNum = transferDegree(jobDegree)
        resumeHigh = resumeNum[0]
                
        for jobn in jobNum:
            if resumeHigh >= jobn : 
                return 1
             
        return 0
        
    def getMajorSim(self, resumeModel,  jobModel):
        resumeMajors = resumeModel.majors 
        jobMajors = jobModel.majors 
        
        for major in resumeMajors:
            if major in jobMajors:
                return 1
                
        for major in resumeMajors:
            if major in CS_RELATED:
                return 0.5
        
        return 0 
        
    def getTitleSim(self, resumeModel,  jobModel):        
        maxvalue = 0
        jobTitle = jobModel.titleModel
    #    print "jobTitle=", jobTitle
        print " resumeModel.titleModels len =" , len(resumeModel.titleModels)
        for resumeTitle in resumeModel.titleModels:
            print "resumeTitle=", resumeTitle
            value = titleSim(jobTitle, resumeTitle)
            if ( value > maxvalue ):
                   maxvalue = value 
        return maxvalue
        
    def getSkillSim(self, resumeModel,  jobModel):
        resumeSkills =  resumeModel.skills
        jobSkills =  jobModel.skills  
        skillLen = len(jobSkills)
        if skillLen == 0 : 
            return 1
        score = 0
        for skill in jobSkills :         
  #          print "jobskill=", skill
            if skill in resumeSkills :
                score += 1
            else :                
                sims = [0]
                for reskill in resumeSkills:   
                    s = self.getOntoDistance( skill, reskill)
                    sims.append(s)
                score += max(sims)
        # print "skill score=" , score
        return score/skillLen 
        
    def getOntoDistance(self, jobskill,reskill):
         if self.pairDict.has_key((jobskill,reskill)) :
 #            print "pairvalue=", self.pairDict[(jobskill,reskill)]
             return self.pairDict[(jobskill,reskill)]
         if self.pairDict.has_key((reskill, jobskill )) :
 #            print "pairvalue=", self.pairDict[(reskill, jobskill )] 
             return self.pairDict[(reskill, jobskill )] 
         
         ref_jobskill =  self.ontology.toURIRef(jobskill)
         ref_reskill = self.ontology.toURIRef(reskill)
         
         if self.ontology.isSuperClass(ref_reskill,ref_jobskill ):
  #           print reskill, jobskill , "superclass"
             return 1
         else: 
             return 0
          
            
    def match_jobColl(self, resumeModel, jobColl):
         jobscore = {}
         for jobModelDict in jobColl.find():
             jid = str(jobModelDict["_id"])
             # print "jid=", jid
             jobModel = JobModel(jid)
             jobModel.deserialize(jobModelDict)
             score = int (self.getSimilarity( resumeModel,  jobModel )*100) 
             
          #   print jid , "--->" ,score
             if (score > 0):
               jobscore[jid] = score
         jobscore =  sorted(jobscore.items(), key=operator.itemgetter(1), reverse= True)     
         return jobscore
         
    def match_jobModels(self, resumeModel, jobModels):
         jobscore = {}
         for jobModelDict in jobModels:
             jid = str(jobModelDict["_id"])
             # print "jid=", jid
             jobModel = JobModel(jid)
             jobModel.deserialize(jobModelDict)
             score = int (self.getSimilarity( resumeModel,  jobModel )*100) 
             
          #   print jid , "--->" ,score
             if score > 0 :
                jobscore[jid] = score
         jobscore =  sorted(jobscore.items(), key=operator.itemgetter(1), reverse= True)     
         return jobscore
         
    def match_jobsr(self, resumeModel, jobColl):
         jobscore = {}
         for jobModelDict in jobColl.find():
             jid = str(jobModelDict["_id"])
             # print "jid=", jid
             jobModel = JobModel(jid)
             jobModel.deserialize(jobModelDict)
             score = random.randint(1, 90)             
          #   print jid , "--->" ,score
             jobscore[jid] = score
         jobscore =  sorted(jobscore.items(), key=operator.itemgetter(1), reverse= True)     
         return jobscore
