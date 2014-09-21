# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 18:17:56 2014

@author: dlmu__000
"""
from commonmodel import CommonModel

class ResumeModel(CommonModel):
    
    def __init__(self, jobid):
        CommonModel.__init__(self)
        self.jobid = jobid
            
    def serialize(self):
        objDict = CommonModel.serialize(self)
        objDict["_id"] = self.jobid        
        return objDict
