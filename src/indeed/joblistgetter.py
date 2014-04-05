# -*- coding: utf-8 -*-
"""
Created on Wed Apr 02 23:09:09 2014

@author: dlmu__000
"""
import urllib
import json
import pymongo
from dbclient import DbClient 

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
          
    def setCity(self, _city):
         self.base_params["l"] = _city
          
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
     #   print 'url =', url
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
            try:
                collection.insert(job)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                #print e
                ()
        return i
    
    def processCity(self, collection, _city ):
         self.setCity(_city)
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
         print " %s get %d jobs, save %d jobs " %(_city, get_sum, save_sum)
         return (get_sum, save_sum)
       
def main():
     cities = ['MoutainView, CA', 'Seattle, WA', 'San Diego, CA', 'San Francisco, CA', 'Austin, TX',
               'San Jose, CA','Portland, OR',' New York, NY','Houston, TX','Boston, MA', 
               'Davis, CA', 'Palo Alto, CA', ' Irvine, CA', 'Olathe, KS', 'Columbia, MD', ' Atlanta, GA' ]
     

     cities = [ 'Austin, TX',
               'San Jose, CA','Portland, OR',' New York, NY','Houston, TX','Boston, MA', 
               'Davis, CA', 'Palo Alto, CA', ' Irvine, CA', 'Olathe, KS', 'Columbia, MD', ' Atlanta, GA' ]
            
     _pageSize = 25 
     _fromage = 30 
     _location = 94040
     _radius = 25
     _query = "software engineer"
     
     collectionName = "job_se_10city"
     indeedClient= ApiClient(_query, _pageSize, _fromage, _location, _radius )
    # client.getPage(0)
     dbClient = DbClient('localhost', 27017, "jobaly")
     collection = dbClient.getCollection(collectionName)
     for city in cities:
         print "-----prcoss city %s -------" %city
         indeedClient.processCity(collection,city)
    
if __name__ == "__main__": 
    main()