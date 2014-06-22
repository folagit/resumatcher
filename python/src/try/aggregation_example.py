# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 12:41:42 2014

@author: dlmu__000
"""

from pymongo import MongoClient
db = MongoClient().aggregation_example 
# db.drop_collection("things")
db.things.remove()
db.things.insert({"x": 1, "tags": ["dog", "cat"]})
db.things.insert({"x": 2, "tags": ["cat"]})
db.things.insert({"x": 2, "tags": ["mouse", "cat", "dog"]})
db.things.insert({"x": 3, "tags": []})

from bson.son import SON
result = db.things.aggregate([
       {"$unwind": "$tags"},
       {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
     ])
     
print type(result)

if (result["ok"] == 1) :
    relist = result["result"]
    for item in relist:
        print item
     
     