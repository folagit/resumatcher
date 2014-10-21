# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 23:39:03 2014

@author: dlmu__000
"""

from dbclient import DbClient

def copyCollection(srcColl, targetColl, size):
    result = srcColl.find()
    i = 1
    for item in result:
        targetColl.save(item)
        if i > size: 
            break
        else:
            i += 1
        
def copyCollections(targetClient, targetCollName, srcClient, srcCollnames, size):
    targetColl = targetClient.getCollection(targetCollName)  
    
    for srcName in srcCollnames:
        srcColl = srcClient.getCollection(srcName) 
        copyCollection(srcColl, targetColl)
       
            
def main(): 
    targetDb = "jobaly"
    targetClient = DbClient('localhost', 27017, targetDb) 
    srcDb = "jobaly_daily" 
    srcClient = DbClient('localhost', 27017, srcDb)
    
    targetCollName = "job1000"     
    srcCollnames = "daily_job_info_2014-06-16"
    
    srcColl = srcClient.getCollection(srcCollnames)
    targetColl = targetClient.getCollection(targetCollName)
    
    size = 1000 
    copyCollection(srcColl, targetColl, size)

    
if __name__ == "__main__": 
    main()   