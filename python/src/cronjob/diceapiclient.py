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
import datetime
import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
import jobaly.utils


class DiceApiClient:
    # the biggest page size maybe 25
    def __init__(self,  _params=None  ):
           
        self.url_pre = 'http://service.dice.com/api/rest/jobsearch/v1/simple.json?%s'
        self.base_params = { 
          'v' : '2',
          'country': 'US',
          'sort' : "1",
          'sd' : 'd',
          'age' : '1' ,
          'pgcnt': '50' }
          
        if _params is not None:
            self.base_params.update(_params)
        self.pageSize = int(self.base_params["pgcnt"])    
      
    def setCity(self, _loc):
         self.base_params["city"] = _loc
         
    def setState(self, _loc):
         self.base_params["state"] = _loc
         
    def setFromAge(self, _age):
         self.base_params["age"] = _age
                
    def setParam(self, key, value):
         self.base_params[key] = value
         
    def setSearchText(self, txt):
        self.base_params["text"] = txt
    
    def buildQuery(self, keywords, params=None):
        q = keywords
        if params is not None:
            for k,v in params.iteritems(): 
                q += (" " + k+":"+v)
        return q
         
    def getPage(self, pageNo):
        params = self.base_params.copy()
        params['page'] = pageNo
        content = self.makeRequest(params)
        
        json_data = json.loads(content)   
        totalResults = int (json_data["count"])
    #    print "totalResults=",totalResults
        firstno = int (json_data["firstDocument"])
        lastno = int (json_data["lastDocument"])
    #    print "end=",end                      
    #    print json_data                 
    #    has_more = (end < totalResults )
    #    print "has_more= " , has_more        
        atend = ( lastno == totalResults ) 
        if "resultItemList" in json_data:            
            return (json_data["resultItemList"],totalResults, lastno)
        else : 
            return ([],totalResults, lastno)
       
        
    def makeRequest(self,params):
        param_str = urllib.urlencode(params)  
        url = self.url_pre % param_str
        retry = True
        print 'url =', url
        while (retry):
            try : 
                response = urllib.urlopen(url)
                content = response.read()                
                retry = False
            except IOError as e:
                print e
       #     print content
        return content
 
    def savePage(self,  collection, items ):
        i = 0
        for job in items:
       #     print job["jobkey"]
        #    job["_id"] = job["jobkey"]
            job["state"] = self.base_params["state"]
        #    job["_q"] = self.base_params["text"]
        #    print job["detailUrl"]
            jobkey = job["detailUrl"][31:]           
            qmi = jobkey.find("?")
            jobkey = jobkey[0:qmi]
       #     print jobkey
            job["_id"] = jobkey
            job["jobkey"] = jobkey
            try:
                collection.insert(job)
                i+=1
            except pymongo.errors.DuplicateKeyError as e: 
                print e
                pass
        return i
    
    def processQuery(self, collection ):
    #     self.setParam(key,value)
         pg = 0
         count = 10
         end = 0
         get_sum = 0
         save_sum = 0
         while ( count != end ):
            last_end = end
            pg +=1
       #     print "--- getting page %d ---" %pg
            items,count, end = self.getPage(pg)
            
       #     print "--- page %d has %d jobs ---" %(pg,len(items))
            get_sum +=  len(items)
            i = self.savePage(collection,items) 
       #     print "--- page %d has save %d jobs " %(pg,i)
            save_sum += i
         print "state %s get %d jobs, save %d jobs " %( self.base_params["state"], get_sum, save_sum)
         return (get_sum, save_sum)
         
    def getQueryResultNum(self, key, value ):
        self.setParam(key,value)             
        content = self.makeRequest(self.base_params)        
        json_data = json.loads(content)   
        totalResults = int (json_data["totalResults"])
        return totalResults


def getJobList(listCollectionName):
   
    print " --- get daily job by language and top cities---"
               
   # lang_names = jobaly.utils.loadArrayFromFile("lang_list.txt")  
    states = jobaly.utils.loadArrayFromFile("state_list.txt")  
   
    diceClient= DiceApiClient( { "age" : "1"    } )  
    dbClient = DbClient('localhost', 27017, "jobaly_daily")
    collection = dbClient.getCollection(listCollectionName)   
    
    for state in states:
       diceClient.setState(state)             
       print "-----prcoss location %s  -------" % (state) 
       diceClient.processQuery(collection)

def testGetJobList():
    today = datetime.date.today()    
    listCollectionName = "daily_dice_list_"+str(today)
    print listCollectionName
    getJobList(listCollectionName) 

def testgetPage():
    
    diceClient = DiceApiClient()
    diceClient.setState("TX")
    diceClient.setSearchText("Python")
    jobs,lastno = diceClient.getPage(3) 
    print lastno
    print len(jobs)
    
def testProcessQuery():
    today = datetime.date.today()    
    listCollectionName = "daily_dice_list_"+str(today)
    listCollectionName = "daily_dice_list_"+"test"
    
    print listCollectionName 
    dbClient = DbClient('localhost', 27017, "jobaly_daily")
    collection = dbClient.getCollection(listCollectionName) 
    diceClient = DiceApiClient()
    diceClient.setState("TN") 
    print diceClient.processQuery(collection)

def main(): 
    testGetJobList()
    
    
if __name__ == "__main__": 
    main()