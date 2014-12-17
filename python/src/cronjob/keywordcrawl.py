import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
import jobaly.utils
import jobinfo_daily 
import indeedcrawler 
import datetime
import time
import os
from indeedcrawler import  IndeedCrawler 


def crawlIndeed(collection, keyList, locList, days=1):
    crawler = IndeedCrawler()
    crawler.base_params.pop("sort", None)
    crawler.setPageSize(50)
    crawler.setCollection(collection)
    crawler.setFromAge(days)
    
    for city in locList:
       crawler.setLocation(city) 
       for lang in keyList:
           crawler.setKeyword(lang)
           print "-----prcoss location %s with keyword %s -------" % (city, lang) 
           crawler.makeOneQuery(crawler.saveToDb)        
    


def getJobList( dbClient, listCollectionName, days, keyword ):
     lang_names =  [keyword]
     cities = ["Austin, TX"]
     
  #   lang_names = jobaly.utils.loadArrayFromFile("test_lang_list.txt")  
  #   cities = jobaly.utils.loadArrayFromFile("test_loc_list.txt") 
    
     listCollection = dbClient.getCollection(listCollectionName)      
     start_time = time.time()
     print "---- start get job list ----"
   #  getJobList(listCollectionName) 
 
     crawlIndeed(listCollection, lang_names, cities, days ) 
     t =  time.time() - start_time 
     print "---- finish get job list, use %s seconds  ----" %t
     
def getJobInfo(dbClient, listCollectionName, infoCollectionName ):
     print 
     print
     listCollection = dbClient.getCollection(listCollectionName)   
     infoCollection = dbClient.getCollection(infoCollectionName)
     start_time = time.time()     
     print "---- start get job info ----"
     jobinfo_daily.getJobInfo(dbClient, listCollection, infoCollection,1)
     t =  time.time() - start_time
     print "---- finish get job info, use %s seconds  ----" %t

def main():
     t =  datetime.datetime.now()
     print "start at:" , t  
     today = datetime.date.today()  
     keyword = "web developer"
     keyword = "python"
     keyword = "web"
     keyword = "javascript"
     name = keyword.split()[0]
     listCollectionName = "keyword_job_"+name
     print "list collection name:", listCollectionName
     infoCollectionName = "keyword_info_"+name
     print "info collection name:", infoCollectionName
     
     dbClient = DbClient('localhost', 27017, "jobaly")
     getJobList( dbClient, listCollectionName, 6, keyword )
     getJobInfo( dbClient, listCollectionName, infoCollectionName )      
  
   
  #   os.environ["LIST_COLL_NAME"] = listCollectionName
  #   os.environ["INFO_COLL_NAME"] = infoCollectionName
  #   os.system("bash")     
 
     t =   datetime.datetime.now()
     print "end at:" , t 
    
if __name__ == "__main__": 
    main()
