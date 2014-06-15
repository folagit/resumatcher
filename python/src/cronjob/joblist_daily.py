import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from apiclient import ApiClient
import jobaly.utils
import datetime

def getJobList(listCollectionName):
   
    print " --- get daily job by language and top cities---"
               
    lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
    cities = jobaly.utils.loadArrayFromFile("state_list.txt")  
    
   # lang_names = jobaly.utils.loadArrayFromFile("test_lang_list.txt")  
   # cities = jobaly.utils.loadArrayFromFile("test_loc_list.txt") 
    
    indeedClient= ApiClient(  { "fromage" : "1"    }   )
    # client.getPage(0)
    dbClient = DbClient('localhost', 27017, "jobaly_daily")
    collection = dbClient.getCollection(listCollectionName)   
    
    for city in cities:
       indeedClient.setLocation(city) 
       for lang in lang_names:
           q = indeedClient.buildQuery(lang)
           print "-----prcoss location %s with language %s -------" % (city, lang) 
           indeedClient.processQuery(collection, "q", q)

def main(): 
    today = datetime.date.today()    
    listCollectionName = "daily_job_list_"+str(today)
    print listCollectionName
    getJobList(listCollectionName) 
    
if __name__ == "__main__": 
    main()
