# -*- coding: utf-8 -*-
"""
Created on Sun Apr 06 20:10:29 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02 23:09:09 2014

@author: dlmu__000
"""
import urllib
import json
import pymongo

class ApiClient:
    # the biggest page size maybe 25
    def __init__(self,  _params=None  ):
           
        self.url_pre = 'http://api.indeed.com/ads/apisearch?%s'
        self.base_params = {'publisher' : '3139916985086815',
          'v' : '2',
          'format' : "json",
          'sort' : "date",
          'fromage' : 1,
          'userip':'74.192.206.241',
          'useragent' : 'Mozilla/%2F4.0%28Firefox%29',
          'start': '0'  ,
          'limit': 25, #page size
          'fromage':'50',
          'q': "software engineer",          
          'radius': 25 }
        if _params is not None:
            self.base_params.update(_params)
        self.pageSize = int(self.base_params["limit"])    
      
    def setLocation(self, _loc):
         self.base_params["l"] = _loc
         
    def setFromAge(self, _age):
         self.base_params["fromage"] = _age
                
    def setParam(self, key, value):
         self.base_params[key] = value
    
    def buildQuery(self, keywords, params=None):
        q = keywords
        if params is not None:
            for k,v in params.iteritems(): 
                q += (" " + k+":"+v)
        return q
         
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['start'] = str(pageNo*self.pageSize)
        content = self.makeRequest(params)
        
        json_data = json.loads(content)   
        totalResults = int (json_data["totalResults"])
    #    print "totalResults=",totalResults
        end = int (json_data["end"])
    #    print "end=",end                      
    #    print json_data                 
    #    has_more = (end < totalResults )
    #    print "has_more= " , has_more        
       
        if "results" in json_data:            
            return (json_data["results"],end)
        else : 
            return ([],end)
       
        
    def makeRequest(self,params):
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
        retry = True
      #  print 'url =', url
        while (retry):
            try : 
                response = urllib.urlopen(url)
                content = response.read()                
                retry = False
            except IOError as e:
                print e
     #       print content
        return content
 
    def savePage(self,  collection, items ):
        i = 0
        for job in items:
       #     print job["jobkey"]
            job["_id"] = job["jobkey"]
            job["_q_loc"] = self.base_params["l"]
            job["_q"] = self.base_params["q"]
            
            try:
                collection.insert(job)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                #print e
                pass
        return i
    
    def processQuery(self, collection, key, value ):
         self.setParam(key,value)
         pg = 0
         last_end = -100
         end = 0
         get_sum = 0
         save_sum = 0
         while (last_end != end):
            last_end = end
            pg +=1
       #     print "--- getting page %d ---" %pg
            items, end = self.getPage(pg)
            
       #     print "--- page %d has %d jobs ---" %(pg,len(items))
            get_sum +=  len(items)
            i = self.savePage(collection,items) 
       #     print "--- page %d has save %d jobs " %(pg,i)
            save_sum += i
         print " %s get %d jobs, save %d jobs " %( value, get_sum, save_sum)
         return (get_sum, save_sum)
         
    def getQueryResultNum(self, key, value ):
        self.setParam(key,value)             
        content = self.makeRequest(self.base_params)        
        json_data = json.loads(content)   
        totalResults = int (json_data["totalResults"])
        return totalResults
