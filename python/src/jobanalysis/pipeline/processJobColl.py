# -*- coding: utf-8 -*-
"""
Created on Tue Oct 21 13:54:02 2014

@author: dlmu__000
"""

import re
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from jobaly.db.dbclient import DbClient
from flask.indexer import createIndex
from jobprocess import processjobs

def createJobIndex():
    dbClient = DbClient('localhost', 27017, "jobaly")  
    collname = "job1000"
    coll = dbClient.getCollection(collname)
     
    createIndex(coll)

def copyColl(srcColl,  targetColl, size ):
    result = srcColl.find()
    i = 1
    for item in result:
        if item.has_key("job_title"):
            item["jobtitle"] =  item["job_title"]
        targetColl.save(item)
        if i > size: 
            break
        else:
            i += 1

def createModelColl():
    dbname = "jobaly"
    collname = "job100"
    processjobs( dbname, collname )
     
def processJobColl(): 
    
    
    srcDb = "jobaly_daily" 
    srcCollnames = "daily_job_info_2014-06-16"    
    srcDb = "jobaly_daily_test" 
    srcCollnames = "daily_job_webdev" 
    srcClient = DbClient('localhost', 27017, srcDb)
    srcCollnames = "daily_job_info_2014-06-16"    
    srcColl = srcClient.getCollection(srcCollnames)
    
    targetDb = "jobaly"
    targetCollName = "job100" 
    targetClient = DbClient('localhost', 27017, targetDb)
           
    targetColl = targetClient.getCollection(targetCollName)
    
    size = 15 
  #  copyColl(srcColl,  targetColl, size)
    processjobs( targetDb, targetCollName )
   # createIndex(targetColl) 
    
def main():
    processJobColl()
     
if __name__ == "__main__": 
    main() 