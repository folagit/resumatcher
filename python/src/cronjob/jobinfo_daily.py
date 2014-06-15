# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 20:47:09 2014

@author: dlmu__000
"""
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
import Queue
import threading
from getjobinfo import IndeedPageGetter
import datetime
from apiclient import ApiClient
import jobaly.utils
import datetime

class JobGetter(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, infoCollection):
       threading.Thread.__init__(self)
       self.queue = queue
       self.getter = IndeedPageGetter(infoCollection)
       
    def run(self):
      while True:
        #grabs host from queue
         page,pageNo = self.queue.get()
         self.getter.processPage(page,pageNo)
         self.queue.task_done()       

def getJobInfo(listCollectionName, infoCollectionName):
    
     dbClient = DbClient('localhost', 27017, "jobaly_daily")
     collection = dbClient.getCollection(listCollectionName)
     infoCollection = dbClient.getCollection(infoCollectionName)
     
     pageSize = 20 
     pageNo = 1
     has_more = True
     pageNum = 10000
     find_sort = None
     find_spec=None

     threadNum = 10
     queue = Queue.Queue()
     for i in range(threadNum):
        t = JobGetter(queue,infoCollection)
        t.setDaemon(True)
        t.start()     
     
     while has_more and pageNo <= pageNum :
        page = dbClient.getPage(collection, find_spec,find_sort, pageSize, pageNo)    
        queue.put( (page,pageNo) )       
        pageNo+=1 
        count =  page.count(with_limit_and_skip = True)
     #   print "count=",count
        if ( count < pageSize ) :
            has_more = False            
     queue.join()   
         
def main():
     
     today = datetime.date.today()    
     listCollectionName = "daily_job_list_"+str(today)
     print listCollectionName
     infoCollectionName = "daily_job_info_"+str(today)
     print infoCollectionName
     getJobInfo(listCollectionName, infoCollectionName)
     
    
if __name__ == "__main__": 
    main()
