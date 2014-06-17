import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from jobinfo_daily import *
from indeedcrawler import *
import time

def main():
     days = 1
     today = datetime.date.today()    
     listCollectionName = "daily_job_list_"+str(today)
     print "list collection name:", listCollectionName
     infoCollectionName = "daily_job_info_"+str(today)
     print "info collection name:", infoCollectionName
     
     lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
     cities = jobaly.utils.loadArrayFromFile("loc_list.txt")  
  
     dbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     listCollection = dbClient.getCollection(listCollectionName)  
    
     start_time = time.time()
     print "---- start get job list ----"
   #  getJobList(listCollectionName) 
     crawlIndeed(listCollection, lang_names, cities,days ) 
     t =  time.time() - start_time 
     print "---- finish get job list, use %s seconds  ----" %t
     
     print 
     print
     infoCollection = dbClient.getCollection(infoCollectionName)
     start_time = time.time()     
     print "---- start get job info ----"
     getJobInfo(dbClient, listCollection, infoCollection)
     t =  time.time() - start_time
     print "---- finish get job info, use %s seconds  ----" %t
    
     
    
if __name__ == "__main__": 
    main()
