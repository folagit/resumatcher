# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 17:26:04 2014

@author: dlmu__000
"""

CS_RELATED=set(["MAJOR_EE", "MAJOR_INFO", "MAJOR_CE" ])
  
    
def tranferDegree(degees):
    degreeDict = {"HS_LEVEL": 1,  "AS_LEVEL": 2,  "BS_LEVEL": 3, "MS_LEVEL": 4, "PHD_LEVEL": 5, "GRAD_LEVEL": 6 }
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
        resumeDegree = resumeModel.degrees
        jobDegree = jobModel.degrees        
        resumeNum = tranferDegree(resumeDegree)
        jobNum = tranferDegree(jobDegree)
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
        return 1 
        
        