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
from jobaly.db.collutils import copyCollection
from flask.indexer import createIndex
from jobprocess import processjobs

def createJobIndex():
    dbClient = DbClient('localhost', 27017, "jobaly")  
    collname = "job1000"
    coll = dbClient.getCollection(collname)
     
    createIndex(coll)

def copyColl():
    targetDb = "jobaly"
    targetClient = DbClient('localhost', 27017, targetDb) 
    srcDb = "jobaly_daily" 
    srcClient = DbClient('localhost', 27017, srcDb)
    
    targetCollName = "job1000"     
    srcCollnames = "daily_job_info_2014-06-16"
    
    srcColl = srcClient.getCollection(srcCollnames)
    targetColl = targetClient.getCollection(targetCollName)
    
    size = 1000 
    
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
    collname = "job1000"
    processjobs( dbname, collname )
     
def main(): 
   # copyColl()
    createModelColl()
  # createJobIndex()
     
if __name__ == "__main__": 
    main() 