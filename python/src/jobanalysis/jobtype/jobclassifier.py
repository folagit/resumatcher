# -*- coding: utf-8 -*-
"""
Created on Wed Dec 24 11:00:34 2014

@author: dlmu__000
"""

jobtype=["WEB_DEV", "PHP_DEV","JAVA_DEV", "PYTHON_DEV" , "MOBILE_DEV", "CLOUD_DEV"]

def classifyJob(jobModel): 
    titleModel = jobModel.titleModel 
    jobModel.summary = titleModel.copy()
    return 
    if titleModel["role"] == "DEV" :
        processDev(jobModel)
        
        
def processDev(jobModel):
    titleModel = jobModel.titleModel 
    sumModel = jobModel.summary
    
     
    