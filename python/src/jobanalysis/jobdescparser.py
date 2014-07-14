# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 17:12:39 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient
import json
import re
import operator
from bs4 import BeautifulSoup
import bs4
import nltk
from textblob import TextBlob

class JobDesc():
    
    class Paragraph():
          def __init__(self, complete, eles=None ):
              self.complete = complete
              if eles is None :
                  self.eles = []
              else :
                  self.eles = eles
              
          def addEle(self, ele):
              self.eles.append(ele)
    
    def __init__(self, toptag ):
         self.topTag = toptag
         self.sents = []
         self.sentElements = []
         self.parse(toptag)
         print "*********len of self.sentElements =", len(self.sentElements)
         self.createParagraphs()
         self.printParagraphs()
    
    def createParagraphs(self):
        para = self.Paragraph(False, self.sentElements[:] ) 
        self.paragraphs = [para ]       
        self.applyRule_1()  
        self.applyRule_2() 
               
    def applyRule_1(self  ):   
        i = 0 
        while i < len(self.paragraphs) :           
            para = self.paragraphs[i]          
            j = 0
            while not para.complete and j < len (para.eles): 
        #       print "i=",i,'  j=',j
               ele = para.eles[j]             
               if len(ele.sents) > 1  and ele.parent is  self.topTag :
                   del  self.paragraphs[i] 
                   if len(para.eles[j+1:]) > 0 :
                       p3 =  self.Paragraph(False,para.eles[j+1:])
                       self.paragraphs.insert(i,p3)
                   p2 =  self.Paragraph(True, para.eles[j:j+1])
                   self.paragraphs.insert(i,p2)
                   if len(para.eles[:j]) > 0 :
                       p1 =  self.Paragraph(False,para.eles[:j])
                       self.paragraphs.insert(i,p1)                                       
                   break
               j+=1
            i+=1      
    
    def applyRule_2(self  ):   
        i = 0 
        while i < len(self.paragraphs) :           
            para = self.paragraphs[i]          
            j = 0
            while not para.complete and j < len (para.eles): 
        #       print "i=",i,'  j=',j
               ele = para.eles[j]   
          #     print type(ele.parent) , ele.parent.name
               if  ele.parent.name == "li"  :
              #     print ele.parent.name
                   start = j
                   end = start+1
              #     print "**ele=",ele
                   while end < len(para.eles) and  para.eles[end].parent.parent == ele.parent.parent :
                       end+=1
                   end-=1 
                   del  self.paragraphs[i] 
                   if len(para.eles[end+1:]) > 0 :
                       p3 =  self.Paragraph(False,para.eles[end+1:])
                       self.paragraphs.insert(i,p3)
                   p2 =  self.Paragraph(True, para.eles[start:end+1])
                   self.paragraphs.insert(i,p2)
                   if len(para.eles[:start]) > 0 :
                       p1 =  self.Paragraph(False,para.eles[:start])
                       self.paragraphs.insert(i,p1)                                       
                   break
               j+=1
            i+=1        
    
    def printParagraphs(self):
         i = 1
         for para in self.paragraphs:
             print "======== para  ", i, "complete=", para.complete ," ==========="
             j = 1
             for element in para.eles:
                 for sent in element.sents:                    
                    print j, ":", sent.encode("GBK", "ignore")
                    j+=1
             i+=1
             
    def listParagraphs(self):
         paras = []        
         for paragraph in self.paragraphs:             
             para = []
             for element in paragraph.eles:
                para.append(element.sents)
             paras.extend(para)
         return   paras            
        
    def parse(self, element):
        
        if type( element) is bs4.element.NavigableString:
            p = element.string.strip()
            if len(p) == 0 :
                return
            blob = TextBlob(element.string)                
            element.sents = blob.raw_sentences
            if len(element.sents) > 0 :               
                self.sentElements.append(element)
                i = 1
                for sent in element.sents:
                    self.sents.append((sent,element))
           #         print i, ":", sent.encode("GBK", "ignore")
                    i+=1
            #    print "-----------------"
            
            return 
            
        if not hasattr(element, 'contents'):  
            return 
            
        for subcontent in element.contents :
            self.parse(subcontent) 

class JobDescParser():
    
    @staticmethod 
    def parseJobDesc(job):
      #  print job["summary"]
        jobpage = re.sub("<a.*?>|</a>", " ", job["summary"])   
        soup = BeautifulSoup(jobpage)
      #  print soup
      #  print type(soup.contents[0].contents[0])
        jobcontent = soup.contents[0].contents[0].contents[0]
        paragraph = JobDesc(jobcontent)            
        return paragraph    

def testParseAll():
    
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     jid = "9e216b2d65bd864b"
  #   jid = "matrixga/78237-51"
     job = DbClient.findById(newCol,jid)
   #  paragraph = JobParser.parseParagraph(job)
     
     for job in newCol.find(): 
         print "\n\n\n======",job["_id"],"============================\n"
     
         jobDesc = JobDescParser.parseJobDesc(job)
         

def testParseParagraph():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     jid = "9e216b2d65bd864b"
  #   jid = "matrixga/78237-51"
     job = DbClient.findById(newCol,jid)
     jobDesc = JobDescParser.parseJobDesc(job)
     
        
def main(): 
    testParseParagraph()
    
    
if __name__ == "__main__": 
    main()   