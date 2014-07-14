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

class Paragraph():
    
    def __init__(self, toptag ):
         self.topTag = toptag
         self.sents = []
         self.parse(toptag)
        
    def parse(self, element):
        
        if type( element) is bs4.element.NavigableString:
            p = element.string.strip()
            if len(p) == 0 :
                return
            blob = TextBlob(element.string)                
            element.sents = blob.raw_sentences
            i = 1
            for sent in element.sents:
                self.sents.append((sent,element))
                print i, ":", sent.encode("GBK", "ignore")
                i+=1
            print "-----------------"
            return 
            
        if not hasattr(element, 'contents'):  
            return 
            
        for subcontent in element.contents :
            self.parse(subcontent) 

class JobParser():
    
    @staticmethod 
    def parseParagraph(job):
      #  print job["summary"]
        notlist = ["br","img"]
        soup = BeautifulSoup(job["summary"])
      #  print soup
      #  print type(soup.contents[0].contents[0])
        jobcontent = soup.contents[0].contents[0].contents[0]
        paragraph = Paragraph(jobcontent)            
        return paragraph    

def testParseParagraph():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     newCol = srcBbClient.getCollection("daily_job_webdev")       
     jid = "9e216b2d65bd864b"
     jid = "matrixga/78237-51"
     job = DbClient.findById(newCol,jid)
     paragraph = JobParser.parseParagraph(job)
     

    
def main(): 
    testParseParagraph()
    
    
if __name__ == "__main__": 
    main()   