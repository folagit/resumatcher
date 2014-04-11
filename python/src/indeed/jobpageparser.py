# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 09:30:00 2014

@author: dlmu__000
"""

from bs4 import BeautifulSoup

class IndeedParser():
    
     def parsePage(self, page_content,job ):
         
         self.soup = BeautifulSoup(page_content)
         self.findJobTitle(job)
         self.parseLink(job)
         self.parseContent(job)
             
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
        span =  self.soup.select(".summary")[0]
     #   print "summary = %s" %span 
      #  print type(span)
      #  print str(span)
        job["summary"] = str(span )      
        

def main():
    fileName = "..\..\data\job_1.html"
    fileName = "..\..\data\job_2.html"
    parser = IndeedParser()
    with open(fileName) as html_file:
        content = html_file.read()
   #     print content
        job = {}
        parser.parsePage(content,job)
   #     print job
        
if __name__ == "__main__": 
    main()