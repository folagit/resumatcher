# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 18:05:18 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
import modelsimilarity
from jobaly.db.dbclient import DbClient
from model.jobmodel import JobModel
from model.resumemodel import ResumeModel
from modelsimilarity import ModelSimilarity

resumeModel1 = ResumeModel("r001")
resumeModel1.addDegrees(["BS_LEVEL"])
resumeModel1.addMajors(["MAJOR_INFO"])
resumeModel1.addSkills([ "html", "css", "java","ruby", "ror"])

jobModel1 = JobModel("j001")
jobModel1.addDegrees(["BS_LEVEL",  "MS_LEVEL" ])
jobModel1.addMajors(["MAJOR_CE", "MAJOR_RELATED"])
jobModel1.addSkills([ "html", "css", "jquery", "ruby"])

def test_tranferDegree():
    degrees = set(["AS_LEVEL",  "BS_LEVEL", "MS_LEVEL", "GRAD_LEVEL"])
    degreeNum = modelsimilarity.tranferDegree(degrees)
    for num in  degreeNum:
        print num


def test_similarity():
    similarity = ModelSimilarity()    
    result = similarity.getSimilarity(resumeModel1 , jobModel1 )
    print "result=", result
    
def test_match():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     jobCollName = "daily_job_webdev"
     
     jobmodelCollName = jobCollName+"_model"
     collection = srcBbClient.getCollection(jobCollName)
     modelColl = srcBbClient.getCollection(jobmodelCollName)
   #  newCol = srcBbClient.getCollection("daily_job_info_2014-06-16")
      
     similarity = ModelSimilarity()    
     result = similarity.match_jobs(resumeModel1 , modelColl  )
     i = 0
     for key, value in result:
         i += 1
         print i,key, value

test_match()    