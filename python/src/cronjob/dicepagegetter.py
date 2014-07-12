# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 01:18:11 2014

@author: dlmu__000
"""



from bs4 import BeautifulSoup
import urllib2
import traceback
import sys
import httplib

class DiceParser():
    
     def parsePage(self, page_content,job ):
         
         self.soup = BeautifulSoup(page_content)
        # self.findJobTitle(job)
        # self.parseLink(job)
         result  = self.parseContent(job)
         return result           
         
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
         
        divclasses = [".content",".dc_content", ".job_desc",".jobDesc" ]
        divids = ["detailDescription","jobdesc","job","positionDetails","jobDesc"] 
        
        for  divid in divids:
            result = self.soup.find("div", id=divid)
            if result is not None:
               jobdiv =  result
               job["div"] = "id="+divid
               job["summary"] = str(jobdiv )  
               return True  
        
        for  divclass in divclasses:
            result = self.soup.select(divclass)
            if len(result) > 0 :
               jobdiv =  result[0]
               job["div"] = "class="+divclass
               job["summary"] = str(jobdiv )  
               return True          
     
        result = self.soup.find("input", id="searchTerms")
        if result is not None:
            job["div"] = "id="+"searchTerms"
            job["summary"]="BE_REMOVED"
            return False        
        
        print "not find div:", job["detailUrl"]
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
                     job["jobtitle"] = job["jobTitle"] 
                     self.collection.insert(job)
                     i+=1
       #  print "--- job info: %d jobs has been saved for page %d " %(i, pageNo)
             
     def processJob(self, parser, jobItem):
         url = jobItem["detailUrl"]
         jobkey = jobItem["jobkey"]
               
      #   print "jobkey=", jobkey
         page = self.makeHttpRequest(url)
         
         if page == "ERROR" :
             print "-- cannot get page --- "
         else: 
             try:
                 if parser.parsePage(page, jobItem):
                     return jobItem
                 else :
                     return None
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
                print "getjobinfo urllib2.HTTPError, url=", url 
                traceback.print_exc(file=sys.stdout)
            except urllib2.URLError as e:
                print "getjobinfo urllib2.URLError, url=", url 
                traceback.print_exc(file=sys.stdout)
            
            except  httplib.BadStatusLine as e:
                pass                
                
            except  Exception as e:
                 print "getjobinfo  Unexpected error, url=", url 
                 traceback.print_exc(file=sys.stdout)
            
            i+=1
        return "ERROR"



    
def testParser():
   url = "http://www.dice.com/job/result/cybercod/KM-11540593?src=19"
   url = "http://www.dice.com/job/result/RTL86097/8868-1AC3184360951"   
 #  url = "http://www.dice.com/job/result/10290916/Acess_AL"
 #  url = "http://www.dice.com/job/result/10203814/657891"   
   url = "http://www.dice.com/job/result/rhalfint/03931-000010"
   url = "http://www.dice.com/job/result/yohbot/1042161"
   url = "http://www.dice.com/job/result/kforcecx/ITWQG1341670"
   url = "http://www.dice.com/job/result/10117616/14029161"
   url = "http://www.dice.com/job/result/10103934/DC46451DDP6?src=19"  
   pageGetter =  DicePageGetter(None)
   page = pageGetter.makeHttpRequest(url)
 #  print page
   parser = DiceParser()    
   parser.parsePage(page,{"detailUrl":url})
   
def main():     
     testParser()
    
if __name__ == "__main__": 
    main()
