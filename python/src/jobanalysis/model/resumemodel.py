# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 18:17:56 2014

@author: dlmu__000
"""
from commonmodel import CommonModel

class ResumeModel(CommonModel):
    
    def __init__(self, resumeid=None):
        CommonModel.__init__(self)
        self.resumeid = resumeid
        self.titleModels = []
            
    def serialize(self):
        objDict = CommonModel.serialize(self)
        objDict["_id"] = self.resumeid  
        objDict["titleModels"] = self.titleModels
        return objDict
   
    def deserialize(self, dictModel):
        super(ResumeModel,self).deserialize(dictModel)
        self.titleModels = dictModel["titleModels"]