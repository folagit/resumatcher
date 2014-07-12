import Queue
import threading
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from dicepagegetter import DicePageGetter
import datetime

class JobGetter(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, infoCollection):
       threading.Thread.__init__(self)
       self.queue = queue
       self.getter = DicePageGetter(infoCollection)
       
    def run(self):
      while True:
        #grabs host from queue
         page,pageNo = self.queue.get()
         self.getter.processPage(page,pageNo)
         self.queue.task_done()       

def getJobInfo(dbClient, listCollection, infoCollection):
   
     pageSize = 20 
     pageNo = 1
     has_more = True
     pageNum = 10000
     find_sort = None
     find_spec=None

     threadNum = 30
     queue = Queue.Queue()
     for i in range(threadNum):
        t = JobGetter(queue,infoCollection)
        t.setDaemon(True)
        t.start()     
     
     while has_more and pageNo <= pageNum :
        page = dbClient.getPage(listCollection, find_spec,find_sort, pageSize, pageNo)    
        queue.put( (page,pageNo) )       
        pageNo+=1 
        count =  page.count(with_limit_and_skip = True)
     #   print "count=",count
        if ( count < pageSize ) :
            has_more = False            
     queue.join()  
         

def testGetJobInfo():     
     dbClient = DbClient('localhost', 27017, "jobaly_daily")
     today = datetime.date.today()    
     listCollectionName = "daily_dice_list_"+str(today)
     infoCollectionName = "daily_dice_info_"+str(today)
    
     listCollectionName = "daily_dice_list_2014-07-11"
     infoCollectionName = "daily_dice_info_2014-07-11"

     print listCollectionName
     print infoCollectionName
     listCollection = dbClient.getCollection(listCollectionName)   
     infoCollection = dbClient.getCollection(infoCollectionName)
     getJobInfo(dbClient,listCollection, infoCollection)
     
def testProcessPage():
     
     listCollectionName = "daily_dice_list_2014-07-11"
     infoCollectionName = "daily_dice_info_2014-07-11"
    
     dbClient = DbClient('localhost', 27017, "jobaly_daily")
     listCollection = dbClient.getCollection(listCollectionName)
     infoCollection = dbClient.getCollection(infoCollectionName)
     getter = DicePageGetter(infoCollection)

     pageSize = 100 
     pageNo = 1
     has_more = True
     pageNum = 10000
     find_sort = None
     find_spec=None
     while has_more and pageNo <= pageNum :
        page = dbClient.getPage(listCollection, find_spec,find_sort, pageSize, pageNo)    
        getter.processPage(page,pageNo)        
        pageNo+=1 
        count =  page.count(with_limit_and_skip = True)
     #   print "count=",count
        if ( count < pageSize ) :
            has_more = False
  
   
def main():     
     testGetJobInfo()
    
if __name__ == "__main__": 
    main()        