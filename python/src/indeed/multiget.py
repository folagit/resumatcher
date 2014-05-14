# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 20:47:09 2014

@author: dlmu__000
"""

import Queue
import threading
from dbclient import DbClient 
from getjobinfo import IndeedPageGetter

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
         
         
def main():
     
     collectionName = "job_se_10city"
     infoCollectionName = "jobinfo_se_10city"
     
     collectionName = "job_lang_top_corps"
     infoCollectionName = "jobinfo_lang_top_corps"
    
     dbClient = DbClient('localhost', 27017, "jobaly")
     collection = dbClient.getCollection(collectionName)
     infoCollection = dbClient.getCollection(infoCollectionName)
     
     pageSize = 20 
     pageNo = 1
     has_more = True
     pageNum = 10000
     find_sort = None
     find_spec=None

     threadNum = 20
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
    
if __name__ == "__main__": 
    main()
