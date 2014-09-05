# -*- coding: utf-8 -*-
"""
Created on Fri Sep 05 00:03:18 2014

@author: dlmu__000
"""

def preprocess(job):
    return sents
    
def processSents(jobModel, sents):       
     
    for sent in sents:
        if isDegreeSent(sent):
            parseDegree(jobModel, sent )
        if isSkillSent(sent):
            parseSkill(jobModel, sent )
            
    return jobModel 

def isDegreeSent(sent):
    return False  

def isSkillSent(sent):
    return False   

def parseDegree(jobModel, sent ):
    pass
       
def parseSkill(jobModel, sent ):
    pass    

def processTitle(jobModel, sent ):
    pass    