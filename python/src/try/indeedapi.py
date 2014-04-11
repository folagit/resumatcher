# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02 23:09:09 2014

@author: dlmu__000
"""
import urllib
import gzip
import cStringIO
import json
import pymongo
import time

class ApiClient:
    # the biggest page size maybe 25
    def __init__(self, _query, _pageSize, _fromage, _location, _radious  ):
        self.pageSize =  _pageSize
        self.url_pre = 'http://api.indeed.com/ads/apisearch?%s'
        self.base_params = {'publisher' : '3139916985086815',
          'v' : '2',
          'format' : "json",
          'sort' : "date",
          'fromage' : str(_fromage),
          'userip':'74.192.206.241',
          'useragent' : 'Mozilla/%2F4.0%28Firefox%29',
          'start': '0'  ,
          'limit': str(_pageSize),
          'fromage':'50',
          'q': _query,
          'l':str(_location),
          'radius': str(_radious) }
          
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['start'] = str(pageNo*self.pageSize)
        content = self.makeRequest(params)
        
        json_data = json.loads(content)    
    #    print json_data
        
        return 
        has_more = json_data["has_more"]
        print "has_more= " , has_more
        
        if has_more :
            if "items" in json_data:            
                return json_data["items"]
            else : 
                return "NO_ITEMS"
        else:
            return "NO_MORE"
        
    def makeRequest(self,params):
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
        retry = True
     #   print 'url =', url
        while (retry):
            try : 
                response = urllib.urlopen(url)
                content = response.read()                
                retry = False
            except IOError as e:
                print e
            print content
        return content
 
    def savePage(self,  collection, items ):
        i = 0
        for job in items:
        #    print question["question_id"]
            job["_id"] = job["question_id"]
            try:
                collection.insert(question)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                #print e
                ()
        return i
    
    
       
def main():
    
     _pageSize = 25
     _fromage = 3 
     _location = 94040
     _radius = 3
     _query = "software engineer"
     
     client= ApiClient(_query, _pageSize, _fromage, _location, _radius )
     client.getPage(0)
     
     return 
     
     dbClient = DbClient('localhost', 27017, "jobaly")
     collection = dbClient.getCollection("job_se_94040_3")    
     for i in range (2):
         print "---- this is page %d  --- " %i
         client.getPage(i)
     

if __name__ == "__main__": 
    main()