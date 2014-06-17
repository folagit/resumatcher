# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 23:35:32 2014

@author: dlmu__000
"""
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
import jobaly.db.collutils as collutils

def main():
     targetBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     targetColl = targetBbClient.getCollection("test_coll")
     
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily")
     srcColl = srcBbClient.getCollection("daily_job_info_2014-06-04")
  #   collutils.copyCollection(srcColl, targetColl)
     
     srcCollNames = ["daily_job_info_2014-06-04", "daily_job_info_2014-06-05", "daily_job_info_2014-06-06", "daily_job_info_2014-06-08", "daily_job_info_2014-06-10"]
   #  collutils.copyCollections(targetBbClient, "job_info_merge", srcBbClient, srcCollNames)
     
     srcCollNames = ["daily_job_list_2014-06-04", "daily_job_list_2014-06-05", "daily_job_list_2014-06-06", "daily_job_list_2014-06-08", "daily_job_list_2014-06-10"]
     collutils.copyCollections(targetBbClient, "job_list_merge", srcBbClient, srcCollNames)

if __name__ == "__main__": 
    main()