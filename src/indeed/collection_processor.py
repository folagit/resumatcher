# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 17:15:32 2014

@author: dlmu__000
"""
from dbclient import DbClient 
class CollectionPageProcessor():
    
     def __init__(self, _dbClient,collectionName ):
         self.dbClient = _dbClient
         self.collection = self.dbClient.getCollection(collectionName)
       
         
     def process(self, processfun, pageNo = 1,   pageNum=10000, pageSize = 100,  find_spec=None, find_sort = None ):
     
         has_more = True
         while has_more and pageNo <= pageNum :
             page = self.dbClient.getPage(self.collection, find_spec,find_sort, pageSize, pageNo)    
             processfun(self.collection, page,pageNo)        
             pageNo+=1 
             count =  page.count(with_limit_and_skip = True)
             if ( count < pageSize ) :
                has_more = False

def printPageCount(collection, page, pageNo):  
      count =  page.count(with_limit_and_skip = True)
      print "page %d havs count= %d" %(pageNo, count)
    
def main():
     
     collectionName = "jobinfo_se_top_corps"     
     dbClient = DbClient('localhost', 27017, "jobaly")
     pageProcessor = CollectionPageProcessor(dbClient,collectionName )
     pageProcessor.process(printPageCount, pageNo = 1,   pageNum=10)
    
if __name__ == "__main__": 
    main()