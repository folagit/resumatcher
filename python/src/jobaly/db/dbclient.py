# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 20:55:46 2014

@author: dlmu__000
"""

from pymongo import MongoClient

class DbClient:
    
    def __init__(self, host, port, dbName):
         self.client = MongoClient(host, port)
         self.db = self.client[dbName]
    
    def getCollection(self, collection_name):
        return self.db[collection_name]
        
    def getPage(self, collection, find_spec ,find_sort, pageSize, pageNo):
        _skip = (pageNo-1) * pageSize
        page = collection.find(spec=find_spec, sort=find_sort , skip = _skip, limit=pageSize)
        return page          
    
    def getSimplePage(self, collection, pageSize, pageNo): 
        _skip = (pageNo-1) * pageSize
        page = collection.find(spec=None, sort=None , skip = _skip, limit=pageSize)
        return page  
        
    def copyToCollection(self, srcColName, toColName, size):      
        srcCol = self.getCollection(srcColName)
        toCol = self.getCollection(toColName)
        docs = self.getSimplePage(srcCol, size, 1)
        toCol.insert(docs)
        
