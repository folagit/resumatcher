
from jobinfo_daily import *
from indeedcrawler import *
import time

def main():
     
     today = datetime.date.today()    
     listCollectionName = "daily_job_list_"+str(today)
     print "list collection name:", listCollectionName
     infoCollectionName = "daily_job_info_"+str(today)
     print "info collection name:", infoCollectionName
     

     start_time = time.time()
     print "---- start get job list ----"
   #  getJobList(listCollectionName) 
     getJobList_sync(listCollectionName) 
     t =  time.time() - start_time 
     print "---- finish get job list, use %s seconds  ----" %t
     
     print 
     print
     
     start_time = time.time()     
     print "---- start get job info ----"
     getJobInfo(listCollectionName, infoCollectionName)
     t =  time.time() - start_time
     print "---- finish get job info, use %s seconds  ----" %t
    
     
    
if __name__ == "__main__": 
    main()
