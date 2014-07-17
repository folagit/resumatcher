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
from nltk.tokenize import sent_tokenize, word_tokenize
from textblob import TextBlob

class JobDesc():
    
    class Paragraph():
          def __init__(self, complete, eles=None, reason=None ):
              self.complete = complete
              if eles is None :
                  self.eles = []
              else :
                  self.eles = eles
              self.reason = reason
              
          def addEle(self, ele):
              self.eles.append(ele)
    
    def __init__(self, toptag, _id ):
         self._id = _id
         self.topTag = toptag
         self.sents = []
         self.sentElements = []
         self.parse(toptag)
      #   print "*********len of self.sentElements =", len(self.sentElements)
         self.createParagraphs()      
    
    def createParagraphs(self):
     #   para = self.Paragraph(False, self.sentElements[:] ) 
     #   self.paragraphs = [para ]  
        self.paragraphs = self.applyRule_p()    
        self.applyRule_topsents()  
        self.applyRule_li() 
        self.applyRule_2br()
    
    def applyRule_p(self ):
        paragraphs = []
        para = self.Paragraph(False)
        for ele in self.sentElements[:]:            
            if  not (ele.parent.name == "p")  :
                para.addEle(ele)
            else:
                newPara =  self.Paragraph(True,[ele],"p")
                if len(para.eles) > 0 :
                   paragraphs.append(para)
                   para = self.Paragraph(False)
                paragraphs.append(newPara)
        if len(para.eles) > 0 :
                   paragraphs.append(para)
        return paragraphs
               
    def applyRule_topsents(self  ):   
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
                   p2 =  self.Paragraph(True, para.eles[j:j+1],"top_sents")
                   self.paragraphs.insert(i,p2)
                   if len(para.eles[:j]) > 0 :
                       p1 =  self.Paragraph(False,para.eles[:j])
                       self.paragraphs.insert(i,p1)                                       
                   break
               j+=1
            i+=1      
    
    def applyRule_li(self  ):   
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
                   p2 =  self.Paragraph(True, para.eles[start:end+1],"li")
                   self.paragraphs.insert(i,p2)
                   if len(para.eles[:start]) > 0 :
                       p1 =  self.Paragraph(False,para.eles[:start])
                       self.paragraphs.insert(i,p1)                                       
                   break
               j+=1
            i+=1        
    
    def applyRule_2br(self ):   
        i = 0 
        while i < len(self.paragraphs) :           
            para = self.paragraphs[i]          
            j = 0
            while not para.complete and j < len (para.eles): 
        #       print "i=",i,'  j=',j
               ele = para.eles[j]     
            #   print "ele name=", ele.next_sibling.name
               con = ( ele.next_sibling is not None  and \
                       ele.next_sibling.name=="br"    and  \
                     ele.next_sibling.next_sibling is not None and \
                     ele.next_sibling.next_sibling.name=="br" )

               if con :
                   del  self.paragraphs[i] 
                   if len(para.eles[j+1:]) > 0 :
                       p3 =  self.Paragraph(False,para.eles[j+1:])
                       self.paragraphs.insert(i,p3)
                   p2 =  self.Paragraph(True, para.eles[ :j+1 ],"2br")
                   self.paragraphs.insert(i,p2)                                                       
                   break
               j+=1
            i+=1       
    
    def printParagraphs(self):
         i = 1
         for para in self.paragraphs:
             print "======== para  ", i, "complete=", para.complete , "reason=",para.reason, " ==========="
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
                para.extend(element.sents)
             paras.append(para)
         return   paras   

    def listAllSentences(self):
       sents = []
       for paragraph in self.paragraphs:
             for element in paragraph.eles:
                sents.extend(element.sents)
              
       return   sents             
    
    def removeInlineTag(self,parentEle):
        for element in parentEle.contents :
           if type( element) is bs4.element.Tag and \
            ( element.name == "strong" or\
                  element.name == "b" or\
                  element.name == "em" ):
            print   element          
        
    def parse(self, element):
        
   #     if type( element) is bs4.element.Tag: 
   #         self.removeInlineTag(element)        
        if type( element) is bs4.element.NavigableString:
            p = element.string.strip()
            if len(p) == 0 :
                return
       #     blob = TextBlob(element.string)                
       #     element.sents = blob.raw_sentences
            element.sents = sent_tokenize(element.string)
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
        jobpage = re.sub("<strong>|</strong>|<b>|</b>|<em>|</em>", " ", jobpage)
      
        if jobpage.find("<span") == 0:
  #          print "root span"
            jobpage = "<div>"+jobpage[22:-7]+"</div>"
   
        jobpage = re.sub("<span.*?>|</span>", " ", jobpage)
        
        jobpage = re.sub("\n", "", jobpage)
        
  #      print jobpage.encode("GBK", "ignore")
        
        soup = BeautifulSoup(jobpage)
      #  print soup
      #  print type(soup.contents[0].contents[0])
        jobcontent = soup.contents[0].contents[0].contents[0]
        paragraph = JobDesc(jobcontent, job["_id"])            
        return paragraph    

def testParseAll():
    
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
    
     job = DbClient.findById(newCol,jid)
   #  paragraph = JobParser.parseParagraph(job)
     
     for job in newCol.find(): 
         print "\n\n\n======",job["_id"],"============================\n"
     
         jobDesc = JobDescParser.parseJobDesc(job)
         

def testParseParagraph():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     jid = "9e216b2d65bd864b"
     jid = "matrixga/78237-51"
     jid = "cybercod/CN-.NETwebDev-CA3"  
     jid = "f3c336fa35c28771"
     jid = "10116717/638726"
     jid = "ocs/54391"
     jid = "0e230c368a34322b"
     jid = "6718adb8b28b9b39"
     job = DbClient.findById(newCol,jid)
     jobDesc = JobDescParser.parseJobDesc(job)
     jobDesc.printParagraphs()
        
def main(): 
    testParseParagraph()
    
    
if __name__ == "__main__": 
    main()   