# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 18:17:56 2014

@author: dlmu__000
"""
from commonmodel import CommonModel

class ResumeModel(CommonModel):
    
    def __init__(self, resumeid):
        CommonModel.__init__(self)
        self.resumeid = resumeid
            
    def serialize(self):
        objDict = CommonModel.serialize(self)
        objDict["_id"] = self.resumeid        
        return objDict
