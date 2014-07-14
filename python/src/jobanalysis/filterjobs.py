# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 16:24:25 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from bson.son import SON
import json
import re
import operator

def filterWebDeveloper_dice():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily")
     targetBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     srcCol = srcBbClient.getCollection("daily_dice_info_2014-07-11")  
     newCol = targetBbClient.getCollection("daily_job_webdev")       
     
     i = 0
     for job in srcCol.find():
         jobtitle = job["jobtitle"].lower()
         if (jobtitle.find("web") != -1 ) and \
             (jobtitle.find("developer") != -1 ):
                 
                job["url"] = job["detailUrl"] 
                job["detailUrl"] = None
                newCol.insert(job) 
                i+=1
                print i, ":", jobtitle.encode("GBK", "ignore")
                if i == 150: 
                    break

def filterWebDeveloper_indeed():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     targetBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     srcCol = srcBbClient.getCollection("daily_job_2014-06-05")  
     newCol = targetBbClient.getCollection("daily_job_webdev")       
     
     for job in srcCol.find():
         jobtitle = job["jobtitle"].lower()
         if (jobtitle.find("web") != -1 ) and \
             (jobtitle.find("developer") != -1 ):
                print jobtitle.encode("GBK", "ignore")                 
                newCol.insert(job) 
    
    
def main(): 
    filterWebDeveloper_dice()
    
    
if __name__ == "__main__": 
    main()    