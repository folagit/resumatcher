# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 17:26:04 2014

@author: dlmu__000
"""
  
    
def tranferDegree(degees):
    degreeDict = {"HS_LEVEL": 1,  "AS_LEVEL": 2,  "BS_LEVEL": 3, "MS_LEVEL": 4, "GRAD_LEVEL": 5, "PHD_LEVEL": 6 }
    degeesList = list(degees)
    degreeNum = []
    for degree in degeesList:
        degreeNum.append(degreeDict[degree])
    degreeNum = sorted(degreeNum, reverse=True)    
    return degreeNum
  
class ModelSimilarity():
    
    def __init__(self):
        self.weightVector = [ 0.1, 0.1, 0.8 ]

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
        resumeDegree = resumeModel.degree
        jobDegree = jobModel.degree
        
        
        
    def getMajorSim(self, resumeModel,  jobModel):
        return 1 
        
    def getSkillSim(self, resumeModel,  jobModel):
        return 1 
        
        