# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 23:39:03 2014

@author: dlmu__000
"""

def copyCollection(srcColl, targetColl):
    result = srcColl.find()
    for item in result:
        targetColl.save(item)
        
        
def copyCollections(targetDb, targetCollName, srcDb, srcCollnames):
    targetColl = targetDb.getCollection(targetCollName)  
    for srcName in srcCollnames:
        srcColl = srcDb.getCollection(srcName) 
        copyCollection(srcColl, targetColl)
    