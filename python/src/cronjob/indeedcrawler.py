# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 23:15:20 2014

@author: dlmu__000
"""
import urllib
import pymongo
from indeedparser import IndeedParser 
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient     
import jobaly.utils
import datetime
import Queue
import threading


class IndeedCrawler: 
    
     # the biggest page size maybe 25
    def __init__(self,  _params=None  ):
        self.pageSize = 50   
        self.url_pre = 'http://www.indeed.com/jobs?%s'
        self.base_params = {
          'sort' : "date",
          'fromage' : 1,          
          'start': '0'  ,
          'limit': 50, #page size
          'fromage':'1',
          'q': "software engineer",          
          'radius': 25 }
        if _params is not None:
            self.base_params.update(_params)
        self.pageSize = int(self.base_params["limit"])    
      
    def setLocation(self, _loc):
        self.base_params["l"] = _loc
         
    def setFromAge(self, _age):
        self.base_params["fromage"] = _age
                
    def setParam(self, key, value):
        self.base_params[key] = value
         
    def setKeyword(self, _key):
        self.setParam("q",_key)
        
    def setPageSize(self, _size):
        self.pageSize = _size
        self.base_params["limit"] = _size
    
    def buildQuery(self, keywords, params=None):
        q = keywords
        if params is not None:
            for k,v in params.iteritems(): 
                q += (" " + k+":"+v)
        return q
         
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['start'] = str((pageNo-1)*self.pageSize)
        content = self.makeRequest(params)
     #   print content        
        parser = IndeedParser(content)
        totalNum = parser.totalResultNum
        joblist = parser.getJobs()
        hasMore = parser.hasNext()
        return  (totalNum, hasMore, joblist )
       
        
    def makeRequest(self,params):       
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
        retry = True
        print 'url =', url
        while (retry):
            try : 
                response = urllib.urlopen(url)
                content = response.read()                
                retry = False
            except IOError as e:
                print e
            
        return content
 
    def savePage(self,  collection, items ):
        i = 0
        for job in items:
       #     print job["jobkey"]
            job["_id"] = job["jobkey"]
            job["_q_loc"] = self.base_params["l"]
            job["_q"] = self.base_params["q"]
            
            try:
                collection.insert(job)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                #print e
                pass
        return i
    
    def makeOneQuery(self, resultFunc):
        pageNo = 1
        hasMore = True
        while hasMore:
       #     print "----------------------"
            totalNum, hasMore, joblist  = self.getPage(pageNo)
            resultFunc( pageNo, totalNum,joblist)  
            pageNo += 1
    
    def setCollection(self, coll):
        self.collection = coll
        
    def saveToDb(self, pageNo, totalNum,joblist):     
        n = 0
        for job in   joblist :           
            job["_q_loc"] = self.base_params["l"]
            job["_q"] = self.base_params["q"]
            
            try:
                self.collection.insert(job)
                n+=1
            except pymongo.errors.DuplicateKeyError as e: 
                #print e
                pass
        
        print "---------saveToDb page %s has %s of   %s and total %s" %( pageNo, n, len(joblist), totalNum )
        return n
            
class CrawlerThread(threading.Thread): 
    
    def __init__(self, queue, listCollection):
       threading.Thread.__init__(self)
       self.queue = queue
       self.crawler = IndeedCrawler()
       self.crawler.setCollection(listCollection)
       self.crawler.setPageSize(50)
       
    def run(self):
      while True:
         loc,lang = self.queue.get()
         self.crawler.setLocation(loc) 
         self.crawler.setKeyword(lang)
         self.crawler.makeOneQuery(self.crawler.saveToDb) 
         self.queue.task_done()

def printResult(result): 
    totalNum, hasMore, joblist = result
    print "totalNum = ", totalNum
    print "hasMore = " , hasMore
    print "joblist num = " , len(joblist)
         
def testGetPage(): 
    crawler = IndeedCrawler()
    crawler.setKeyword("pythonewrewrwe")
    crawler.setLocation("CA")  
    crawler.setFromAge("1")
    printResult(crawler.getPage(1))
    
    crawler.setKeyword("java")    
    printResult(crawler.getPage(1))
    
    crawler.setKeyword("python")    
    printResult(crawler.getPage(10))
    
def simpleResultFunc(pageNo, totalNum,joblist):
    print "---------process page %s has %s of total %s" %( pageNo, len(joblist) ,totalNum )
    for job in  sorted(joblist, key=lambda job: job["id"]) :
        print job["id"]

def crawlIndeed(collection, keyList, locList, days=1):
    crawler = IndeedCrawler()
    crawler.setPageSize(50)
    crawler.setCollection(collection)
    crawler.setFromAge(days)
    
    for city in locList:
       crawler.setLocation(city) 
       for lang in keyList:
           crawler.setKeyword(lang)
           print "-----prcoss location %s with keyword %s -------" % (city, lang) 
           crawler.makeOneQuery(crawler.saveToDb)        
    


def getJobList_sync(listCollectionName):
   
    print " --- get daily job by language and top cities---"
               
    lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
    cities = jobaly.utils.loadArrayFromFile("loc_list.txt")  
    
  #  lang_names = jobaly.utils.loadArrayFromFile("test_lang_list.txt")  
  #  cities = jobaly.utils.loadArrayFromFile("test_loc_list.txt") 

    dbClient = DbClient('localhost', 27017, "jobaly_daily")
    collection = dbClient.getCollection(listCollectionName)  
    crawlIndeed(collection, lang_names, cities )  

def getJobList(listCollectionName):
    
     dbClient = DbClient('localhost', 27017, "jobaly_daily")
     collection = dbClient.getCollection(listCollectionName)  
   
     lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
     cities = jobaly.utils.loadArrayFromFile("loc_list.txt")  
     
  #   lang_names = jobaly.utils.loadArrayFromFile("test_lang_list.txt")  
  #   cities = jobaly.utils.loadArrayFromFile("test_loc_list.txt") 
     
     queue = Queue.Queue()  
     for city in cities:        
         for lang in lang_names:
             queue.put( (city,lang) )  
             
     threadNum = 60 
     for i in range(threadNum):
        t = CrawlerThread(queue,collection)
        t.setDaemon(True)
        t.start()    
        
     queue.join()   

def testMakeQuery1():
    crawler = IndeedCrawler()
    crawler.setKeyword("python")
    crawler.setLocation("CA")  
    crawler.setFromAge("1")
    crawler.makeOneQuery(simpleResultFunc)    
    
def testMakeQuery2():
    crawler = IndeedCrawler()
    crawler.setKeyword("scala")
    crawler.setLocation("CA")  
    crawler.setFromAge("1")
    crawler.setPageSize(10)
    crawler.makeOneQuery(simpleResultFunc) 
  #  printResult(crawler.getPage(3))
    
def testMakeQuery3():
    crawler = IndeedCrawler()
    crawler.setKeyword("Visual Basic.NET")
    crawler.setLocation("San Jose, CA")  
    crawler.setFromAge("1")
    crawler.setPageSize(50)
    crawler.makeOneQuery(simpleResultFunc) 
  
def testSave():
    today = datetime.date.today()    
    listCollectionName = "daily_job_list_"+str(today)
    print listCollectionName
    getJobList(listCollectionName) 
    
def main(): 
    testMakeQuery3()
    
if __name__ == "__main__": 
    main()
