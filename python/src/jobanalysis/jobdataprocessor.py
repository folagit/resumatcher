# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 12:51:23 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from bson.son import SON

class JobDataProcessor:
    
    def __init__(self,  collection  ):
          self.collection = collection

    def aggregateTitleToFile(self, fileName): 
        result = self.collection.aggregate([ 
            { "$group" : { "_id"    : "$jobtitle" ,  
                           "number" : { "$sum" : 1 } } 
            },
            { "$sort" : { "number" : -1 } }
            ])
        if (result["ok"] == 1) :
            f = open(fileName, "w")
            relist = result["result"]
            for item in relist:
              #  print item["_id"]
              #   print type(item["number"])
                 line = item["_id"] + ":" + str(item["number"]) + "\n"
#                 print line
                 f.write(line.encode('utf8'))

def main(): 
    listCollectionName = "daily_job_list_2014-06-16"
    dbClient = DbClient('localhost', 27017, "jobaly_daily")
    collection = dbClient.getCollection(listCollectionName) 
    dataProcessor = JobDataProcessor(collection)
    dataProcessor.aggregateTitleToFile("titleList.txt")
    
if __name__ == "__main__": 
    main()