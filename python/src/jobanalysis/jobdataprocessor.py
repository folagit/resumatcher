# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 12:51:23 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from bson.son import SON
import json

class JobDataProcessor:
    
    def __init__(self,  collection  ):
          self.collection = collection

    def aggregateTitleToFile(self, fileName, filetype="json"): 
        result = self.collection.aggregate([ 
            { "$group" : { "_id"    : "$jobtitle" ,  
                           "number" : { "$sum" : 1 } } 
            },
            { "$sort" : { "number" : -1 } }
            ])
        if (result["ok"] == 1) :
            f = open(fileName, "w")
            relist = result["result"]
            
            if (filetype =="json"):
                json.dump(relist, f)
            elif (filetype =="text"):   
                 for item in relist:              
                     line = item["_id"] + ":" + str(item["number"]) + "\n"
                     print line.encode("GBK", "ignore")
                     f.write(line.encode('utf8'))
                 
def main(): 
    listCollectionName = "daily_job_list_2014-06-10"
    dbClient = DbClient('localhost', 27017, "jobaly_daily")
    collection = dbClient.getCollection(listCollectionName) 
    dataProcessor = JobDataProcessor(collection)
    dataProcessor.aggregateTitleToFile("titles//titleList.json")
    dataProcessor.aggregateTitleToFile("titles//titleList.txt", "text")
    
    
if __name__ == "__main__": 
    main()