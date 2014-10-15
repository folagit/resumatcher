# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 22:44:19 2014

@author: dlmu__000
"""
from tfgetter import TfGetter
import irutils

def loadResume(filepath):
    with open (filepath, "r") as myfile:
        data=myfile.read().replace('\n', '')
        return data

class BaseIr():
    
    def __init__(self, jobCollection):
         self.tfgetter =  TfGetter()   
         self.jobCollection = jobCollection
         self.processColl(self.jobCollection)  
         
    def processColl(self, jobcoll ):     
         self.jobs = []        
         self.doc_num = 0
         sum_length = 0
         for item in jobcoll.find(): 
             content = irutils.processText(item["summary"])    
             tokens =  self.tfgetter.getTokens(content)
             tf = self.tfgetter.getTf(tokens)      
   #          print "tf=",  tf
             item['tf'] =  tf
             item['length'] = len(tokens)
             self.jobs.append(item)
             self.doc_num+=1
             sum_length += item['length']
         self.avgLength = sum_length/self.doc_num
         print "self.avgLength =", self.avgLength
    
    def matchResume(self, resume):
        self.calculateScores(resume)
        self.jobs.sort(key=lambda x: x["score"], reverse=True)
        return self.jobs  