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


class DiceParser():
    
     def parsePage(self, page_content,job ):
         
         self.soup = BeautifulSoup(page_content)
        # self.findJobTitle(job)
        # self.parseLink(job)
         result  = self.parseContent(job)
         if not result :
             print "not find div:", job["detailUrl"]
             
     def findJobTitle(self, job ):          
          div = self.soup.find("div", id="job_header")
          job["job_title"] = div.b.font.string
          # print div.b.font.string
          span1 = div.span
          span2 = div.select(".location")[0]
        #  print span1.string
        #  print span2.string
          job["company"] = span1.string
          job["location"] = span2.string
        #   print job       
       
     def parseLink(self,job): 
        aquo = self.soup.find("div", id="bvjl")
        if aquo is not None:
            job["href"] = aquo.a['href'] 
        else :
            job["href"] = "indeed" 
      #  print "aquo.a.href= %s " %aquo.a['href']         
         
     def parseContent(self, job):
        
        result = self.soup.select(".job_description")
        if len(result) > 0 :
           jobdiv =  result[0]
           job["div"] = "class=.job_description"
           job["summary"] = str(jobdiv )            
           return True
         
        result = self.soup.find("div", id="detailDescription")
        if result is not None:
           jobdiv =  result
           job["div"] = "id=detailDescription"
           job["summary"] = str(jobdiv )  
           return True   
        
        result = self.soup.select(".job_desc")
        if len(result) > 0 :
           jobdiv =  result[0]
           job["div"] = "class=.job_desc"
           job["summary"] = str(jobdiv )            
           return True
       
       
        return False  

class DicePageGetter():
    
     def __init__(self, _collection  ):
         self.collection = _collection  
     
     def processPage(self, page, pageNo):
         parser = DiceParser()
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
         url = jobItem["detailUrl"]
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

def testProcessPage():
     
     listCollectionName = "daily_dice_list_2014-07-12"
     infoCollectionName = "daily_dice_info_2014-07-12"
    
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
          
    
def testParser():
   url = "http://www.dice.com/job/result/cybercod/KM-11540593?src=19"
   url = "http://www.dice.com/job/result/RTL86097/8868-1AC3184360951"   
 #  url = "http://www.dice.com/job/result/10290916/Acess_AL"
 #  url = "http://www.dice.com/job/result/10203814/657891"   
   url = "http://www.dice.com/job/result/rhalfint/03931-000010"
   pageGetter =  DicePageGetter(None)
   page = pageGetter.makeHttpRequest(url)
   print page
   parser = DiceParser()    
   parser.parsePage(page,{})
   
def main():   
    testProcessPage()
  #  testParser()
    
if __name__ == "__main__": 
    main()
