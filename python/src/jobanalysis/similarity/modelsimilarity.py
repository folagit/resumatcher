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


degreeDict = {"HS_LEVEL": 1,  "AS_LEVEL": 2,  "BS_LEVEL": 3, "MS_LEVEL": 4, "PHD_LEVEL": 5, "GRAD_LEVEL": 6 }
CS_RELATED=set(["MAJOR_EE", "MAJOR_INFO", "MAJOR_CE" ])
terms=["javascript", "jquery", "html", "css", "java", "jsp", "python", "ruby", "ror"  ]
termsDict={"javascript":0, "jquery":1, "html":2, "css":3, "java":4, "jsp":5, "python":6, "ruby":7, "ror":8  }
similarity_matrix = [[1, 0.1981, 0.2087, 0.2439, 0.0665, 0.0253, 0.0189, 0.023, 0.0031], 
                     [0.1981, 1, 0.0979, 0.1328, 0.0439, 0.0232, 0.0142, 0.0266, 0.0032], 
                     [0.2087, 0.0979, 1, 0.3569, 0.0473, 0.0103, 0.0175, 0.023, 0.0037], 
                     [0.2439, 0.1328, 0.3569, 1, 0.0537, 0.015, 0.0153, 0.0181, 0.0033], 
                     [0.0665, 0.0439, 0.0473, 0.0537, 1, 0.075, 0.0498, 0.0287, 0], 
                     [0.0253, 0.0232, 0.0103, 0.015, 0.075, 1, 0.0025, 0.012, 0.018], 
                     [0.0189, 0.0142, 0.0175, 0.0153, 0.0498, 0.0025, 1, 0.1333, 0.0057], 
                     [0.023, 0.0266, 0.023, 0.0181, 0.0287, 0.012, 0.1333, 1, 0.0147], 
                     [0.0031, 0.0032, 0.0037, 0.0033, 0, 0.018, 0.0057, 0.0147, 1]]  

def transferSkills(skills):
    skillList = set()
    for skill in skills :
  #      skill = skill.encode('ascii', errors='backslashreplace')
        if termsDict.has_key(skill) :
            skillList.add(termsDict[skill])
    return skillList

def transferDegree(degees):
    degeesList = list(degees)
    degreeNum = []
    for degree in degeesList:
        degreeNum.append(degreeDict[degree])
    degreeNum = sorted(degreeNum, reverse=True)    
    return degreeNum
  
class ModelSimilarity():
    
    def __init__(self):
        self.weightVector = [ 0.1, 0.1, 0.8 ]
        self.ontology = ontologylib.createOntology()
        self.pairDict = pairdistance.loadPairValues()

    def getSimilarity(self, resumeModel,  jobModel):
        simVector = [0] * 3
        simVector[0] = self.getDegreeSim(resumeModel,  jobModel)    
        simVector[1] = self.getMajorSim (resumeModel,  jobModel)  
        simVector[2] = self.getSkillSim (resumeModel,  jobModel)  
        
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
        jobHigh = jobNum[0]
        
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
        
    def getSkillSim(self, resumeModel,  jobModel):
        resumeSkills =  transferSkills(resumeModel.skills)
        jobSkills =  transferSkills(jobModel.skills)  
        skillLen = len(jobSkills)
        if skillLen == 0 : 
            return 1
        score = 0
        for skill in jobSkills :            
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
             print "pairvalue=", self.pairDict[(jobskill,reskill)]
             return self.pairDict[(jobskill,reskill)]
         if self.pairDict.has_key((reskill, jobskill )) :
             print "pairvalue=", self.pairDict[(reskill, jobskill )] 
             return self.pairDict[(reskill, jobskill )] 
         
         ref_jobskill =  self.ontology.toURIRef(jobskill)
         ref_reskill = self.ontology.toURIRef(reskill)
         
         if self.ontology.isSuperClass(ref_reskill,ref_jobskill ):
             print reskill, jobskill , "superclass"
             return 1
         else: 
             return 0
          
            
    def match_jobs(self, resumeModel, jobColl):
         jobscore = {}
         for jobModelDict in jobColl.find():
             jid = str(jobModelDict["_id"])
             # print "jid=", jid
             jobModel = JobModel(jid)
             jobModel.deserialize(jobModelDict)
             score = int (self.getSimilarity( resumeModel,  jobModel )*100) 
             
          #   print jid , "--->" ,score
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