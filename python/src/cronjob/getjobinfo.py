# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 01:18:11 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from bs4 import BeautifulSoup
import urllib2
from jobpageparser import IndeedParser

class IndeedPageGetter():
    
     def __init__(self, _collection  ):
         self.collection = _collection  
     
     def processPage(self, page, pageNo):
         parser = IndeedParser()
         i = 0
         for jobitem in page:
             _id = jobitem["_id"]             
             exist = self.collection.find({"_id": _id },{"_id": True}).limit(1)
           #  print exist.count()             
             if exist.count() < 1 :
                 job = self.processJob(parser, jobitem)
                 if job != None :
           #          print job["_id"]
                     job.update(jobitem)
                     self.collection.insert(job)
                     i+=1
         print "--- job info: %d jobs has been saved for page %d " %(i, pageNo)
             
     def processJob(self, parser, jobItem):
         url = jobItem["url"]
         jobkey = jobItem["jobkey"]
         job = {}
         job["_id"] = jobkey         
      #   print "jobkey=", jobkey
         page = self.makeHttpRequest(url)
         
         if page == "ERROR" :
             print "-- cannot get page --- "
         else: 
             try:
                 parser.parsePage(page, job)
                 return job
             except Exception as e:
                 print "job: ", jobkey , "has error:" ,e
         
     def makeHttpRequest(self, url):
        i = 0
        while i < 4: 
            try:
                response = urllib2.urlopen(url) 
                the_page = response.read()
                return the_page
            except urllib2.HTTPError as e:
                print "getjobinfo urllib2.HTTPError", e 
            except urllib2.URLError as e:
                print "getjobinfo urllib2.URLError", e
            except  Exception as e:
                 print "getjobinfo  Unexpected error:", e
            
            i+=1
        return "ERROR"
     
def main():
     
     collectionName = "job_lang_top_corps"
     infoCollectionName = "jobinfo_lang_top_corps"
    
     dbClient = DbClient('localhost', 27017, "jobaly")
     collection = dbClient.getCollection(collectionName)
     infoCollection = dbClient.getCollection(infoCollectionName)
     getter = IndeedPageGetter(infoCollection)

     pageSize = 10 
     pageNo = 149
     has_more = True
     pageNum = 10000
     find_sort = None
     find_spec=None
     while has_more and pageNo <= pageNum :
        page = dbClient.getPage(collection, find_spec,find_sort, pageSize, pageNo)    
        getter.processPage(page,pageNo)        
        pageNo+=1 
        count =  page.count(with_limit_and_skip = True)
     #   print "count=",count
        if ( count < pageSize ) :
            has_more = False
         
    
if __name__ == "__main__": 
    main()
