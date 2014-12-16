# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 23:51:05 2014

@author: dlmu__000
"""

from bs4 import BeautifulSoup 
import sys
import pytz, datetime

class IndeedParser: 
    
    def __init__(self,  html_doc, from_encoding='utf-8' ):
        self.soup = BeautifulSoup(html_doc)
        self.totalResultNum = self._getResultNum()  
        self.adjobs = False
        
    def _getResultNum(self):        
    
        nodiv =  self.soup.find("div", {"id": "no_results"})
        if nodiv is not None:
            return 0                
        rediv = self.soup.find("div", {"id": "searchCount"})
    #    print type(rediv)
    #    print rediv.text
        tokens = rediv.text.split()
    #    print tokens[-1]
        numstr = tokens[-1]
        num = int(numstr.replace(',', ''))
     #   print num
        return num
        
    def hasNext(self):
         npspans = self.soup.findAll("span", { "class" : "np" })
         for span in  npspans:  
             txt = span.text
         #    print span             
             if txt.find(u"Next") != -1 :         
                 return True
         
         return False
        
    def getJobs( self ):        

        if self.totalResultNum == 0 :
            return []
        
        jobdivs = self.soup.findAll("div", { "class" : "row" })
     #   print type(jobdivs)
        joblist = []
        for jobdiv in jobdivs:
           if   not jobdiv.has_attr("data-jk"):
               continue
           if jobdiv.has_attr("id"):   
               job = self.parseJobDiv(jobdiv) 
           elif   self.adjobs :
               job = self.parseAdJobDiv(jobdiv)
           else: 
               continue
           self.completeJob(job)
           joblist.append( job )
        
    #    print len(joblist)
        return joblist
        
    def completeJob(self, job):
        job["jobkey"] = job["_id"]
        job["url"] = "http://www.indeed.com/viewjob?jk="+job["_id"]
     #   print "location=" , job["formattedLocationFull"]        
        addr = job["formattedLocationFull"].split(",")
        if ( len (addr) == 1 ) :
        #    print addr[0]
            if addr[0] == "United States" : 
                print "location is: United States"
        else :
            job["city"] = addr[0].strip()
            st = addr[1].split()
            job["state"] = st[0].strip()
            if len(st)>1:
                job["zip"] = st[1].strip()
            
        job["country"] = "US"
        
        
    def parseDate(self, jobdiv, job ):
        datespan = jobdiv.find("span", { "class" : "date" })
        job["formattedRelativeTime"] = datespan.text
  #      print job["formattedRelativeTime"]
        strs = datespan.text.split()
        if (strs[0][-1] == "+") :
            strs[0] = strs[0][:-1]
      #  print  " inpage = ", strs[0]
        num = int(strs[0])
        
        if strs[1].find("minute") != -1 :
            minutes = num
        if strs[1].find("hour") != -1 :
            minutes = num * 60 
        elif strs[1].find("day") != -1 :
            minutes = num * 24 * 60
        timezone = -6
        t = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        t = t - datetime.timedelta(hours=timezone)
        job["date"] =  t.strftime("%a, %d %b %Y %H:%M:%S GMT")
   #     print job["date"]
        
    def parseJobDiv(self, jobdiv):
       # print type(jobdiv)
       # jobId = jobdiv["class"]
    
        job = {}        
        jobId = jobdiv["data-jk"].strip()
      #  print "id =",jobId
        job["_id"] = jobId        
       
        titleh2 = jobdiv.find("h2", { "class" : "jobtitle" })
      #  print titleh2
        jobtitle = titleh2.text.strip()
            
      #  print "jobtitle =",jobtitle
        
        job["jobtitle"] = jobtitle
        companyspan = jobdiv.find("span", { "itemprop" : "name" })
   #     print companyspan
        company = ""
        if companyspan  is not None:
            try:
                company = companyspan.text.strip()
            except Error as e:
                print e
                
    #    print "company=",company
        job["company"] = company
        locationspan = jobdiv.find("span", { "itemprop" : "addressLocality" })
        location = locationspan.text.strip().replace('\n','')
    #    print location
        job["formattedLocationFull"] = location  
        
        summspan = jobdiv.find("span", { "class" : "summary" })
        job["snippet"] = summspan.text
    #    print "snippet=" , job["snippet"]
    
        self.parseDate(jobdiv, job)        
        return job    
     
    def parseAdJobDiv(self, jobdiv):
        job = {}        
        try:
            jobId = jobdiv["data-jk"].strip()
        #    print "id =",jobId
            job["_id"] = jobId
        except Exception as e:
            print "e=", e
         #   print "jobId =", jobId
            print "div =",  jobdiv
            sys.exit(0)

        titlea = jobdiv.find("a", { "class" : "jobtitle" })
        if (titlea is not None) :
            jobtitle = titlea.text.strip()
       
    #    print "jobtitle =",jobtitle
        
        job["jobtitle"] = jobtitle
        companyspan = jobdiv.find("span", { "class" : "company" })
   #     print companyspan
        company = ""
        if companyspan  is not None:
            try:
                company = companyspan.text.strip()
            except Error as e:
                print e
                
     #   print "company=",company
        job["company"] = company
        locationspan = jobdiv.find("span", { "class" : "location" })
        location = locationspan.text.strip().replace('\n','')
    #    print location
        job["formattedLocationFull"] = location  
        summspan = jobdiv.find("span", { "class" : "summary" })
        job["snippet"] = summspan.text
     #   print "snippet=" ,job["snippet"]
     
        self.parseDate(jobdiv, job)        
        return job
      
      
def main(): 
  #  with open ("page1.html", "r") as htmlfile:
    with open ("page2.html", "r") as htmlfile:
        htmldoc = htmlfile.read()
        parser = IndeedParser(htmldoc)
        print "result num =",parser.totalResultNum 
        print "job result len=" ,len(parser.getJobs())
    #    print " span  np= " , parser.hasNext()
   
    return     
     
    with open ("noresult.html", "r") as htmlfile:
        htmldoc = htmlfile.read()
        parser = IndeedParser(htmldoc)
        print "result num =",parser.totalResultNum
        print "job result len=" ,len(parser.getJobs())
    
if __name__ == "__main__": 
    main()
