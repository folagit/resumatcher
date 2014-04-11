# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:06:53 2014

@author: dlmu__000
"""
from collection_processor import CollectionPageProcessor
from dbclient import DbClient 
import re


class TfGetter():
    
     def __init__(self, _stopwords=[]  ):          
        TfGetter.stopwords = _stopwords
        TfGetter.term_num_docs = {}
    
     @staticmethod
     def processJob(jobitem):
        content =  jobitem["content"]
        tokens =   re.split(' |,|;|\n|!|\r|\||\-|\/|\\\\',content)
        tokens =   TfGetter.filterTokens(tokens)    
        term_freq = {}
        for token in tokens:
            if term_freq.has_key(token):
                term_freq[token] += 1
            else :
                term_freq[token] = 1 
        jobitem["tf"] = term_freq
        
        for key, value in term_freq.iteritems():        
            if TfGetter.term_num_docs.has_key(key):
                TfGetter.term_num_docs[key]+= 1
            else :
                TfGetter.term_num_docs[key] = 1      
        
        return jobitem
          
     @staticmethod       
     def filterTokens( tokens):
          new_tokens = []
          for token in tokens:
              token = token.lower()
        #     print   self.needToBeFilter(token)
              if len(token)> 0:
                  token = re.sub('\.|\)|\(|\:|\-|\_|\?|\!|\>|\<|\"|\[|\]|\~|\'|\*|\=|\{|\}|\$|\#', '', token)
                  token = re.sub('\d|%|\&|\+|\@', '', token)
                
                  if len(token)> 0 and (not token in TfGetter.stopwords) :
                      new_tokens.append(token)
          return new_tokens

  
     @staticmethod
     def processPage(collection, page,pageNo):
         
         i = 0
         for jobitem in page:
     #        print "job: ", jobitem["_id"]
             if  jobitem.has_key("content") :
                 TfGetter.processJob(jobitem)            
                 collection.save(jobitem)
                 i+=1
                     
         print "%d jobs has been saved for page %d " %(i, pageNo)
        
     
     @staticmethod
     def printPageCount(collection, page, pageNo):  
          count =  page.count(with_limit_and_skip = True)
          print "page %d havs count= %d" %(pageNo, count)   

def printDict( the_dict, fileName ): 
    with open(fileName, 'w') as the_file:
        for key in sorted(the_dict.iterkeys()):
            jstr = "%s: %s \n" % (key, the_dict[key])
            try:            
                the_file.write(jstr)  
            except Exception as e:
                print e

def getStopWords(fileName):
    stopwords = {}
    with open(fileName, 'r') as the_file:
        for line in the_file: 
            word = line.strip()
            if not len(word)==0:
               stopwords[word] =  word
    return  stopwords; 

def main():
    
    stopwords = getStopWords("stopwords.txt")
    tfgetter =  TfGetter(stopwords)   
    
    collectionName = "jobinfo_se_top_corps"     
    dbClient = DbClient('localhost', 27017, "jobaly")
    pageProcessor = CollectionPageProcessor(dbClient,collectionName )
    pageProcessor.process(tfgetter.processPage, pageNo = 1, pageNum=100)
    
    printDict( tfgetter.term_num_docs, "term_idf.txt" )
  
        
if __name__ == "__main__": 
    main()  