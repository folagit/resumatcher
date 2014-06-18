import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
import jobaly.utils
import jobinfo_daily 
import indeedcrawler 
import datetime
import time
import os

def getJobList( dbClient, listCollectionName ):
     lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
     cities = jobaly.utils.loadArrayFromFile("loc_list.txt")  
     
  #   lang_names = jobaly.utils.loadArrayFromFile("test_lang_list.txt")  
  #   cities = jobaly.utils.loadArrayFromFile("test_loc_list.txt") 
    
     listCollection = dbClient.getCollection(listCollectionName)      
     start_time = time.time()
     print "---- start get job list ----"
   #  getJobList(listCollectionName) 
     days = 1
     indeedcrawler.crawlIndeed(listCollection, lang_names, cities, days ) 
     t =  time.time() - start_time 
     print "---- finish get job list, use %s seconds  ----" %t
     
def getJobInfo(dbClient, listCollectionName, infoCollectionName ):
     print 
     print
     listCollection = dbClient.getCollection(listCollectionName)   
     infoCollection = dbClient.getCollection(infoCollectionName)
     start_time = time.time()     
     print "---- start get job info ----"
     jobinfo_daily.getJobInfo(dbClient, listCollection, infoCollection)
     t =  time.time() - start_time
     print "---- finish get job info, use %s seconds  ----" %t

def main():
     t =  datetime.datetime.now()
     print "start at:" , t  
     today = datetime.date.today()    
     listCollectionName = "daily_job_list_"+str(today)
     print "list collection name:", listCollectionName
     infoCollectionName = "daily_job_info_"+str(today)
     print "info collection name:", infoCollectionName
     
     dbClient = DbClient('localhost', 27017, "jobaly_daily")
     getJobList( dbClient, listCollectionName )
     getJobInfo( dbClient, listCollectionName, infoCollectionName )      
  
   
  #   os.environ["LIST_COLL_NAME"] = listCollectionName
  #   os.environ["INFO_COLL_NAME"] = infoCollectionName
  #   os.system("bash")     
 
     t =   datetime.datetime.now()
     print "end at:" , t 
    
if __name__ == "__main__": 
    main()
