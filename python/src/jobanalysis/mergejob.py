# -*- coding: utf-8 -*-
"""
Created on Tue Jul 08 22:18:47 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 


def mergeJob(listCol, infoCol, newCol):
    
    for job in listCol.find():        
        jobinfo = infoCol.find_one({"_id": job["_id"]})
        if jobinfo is not None:
            jobinfo.update(job)
            newCol.save(jobinfo)
    
def mergeDailyJob(date):
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily")
     targetBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     listCol = srcBbClient.getCollection("daily_job_list_"+date)  
     infoCol = srcBbClient.getCollection("daily_job_info_"+date)  
     newCol = targetBbClient.getCollection("daily_job_"+date)       
     mergeJob(listCol, infoCol, newCol)
   
def main():
    mergeDailyJob("2014-06-05")
    
   
if __name__ == "__main__": 
    main()
     
     