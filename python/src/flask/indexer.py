# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:30:33 2014

@author: dlmu__000
"""

from whoosh import index 
from whoosh.fields import *
from whoosh.qparser import QueryParser

#from  webapp import dataHandler
from jobaly.db.dbclient import DbClient 
import os

import re
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub(' ', text)

schema = Schema(jobtitle=TEXT(stored=False), jobid=ID(stored=True), content=TEXT)
indexdir = "index"

#searcher = myindex.searcher()
#jobColl = dataHandler.jobCollection

def removeHtml(coll):
    
     for job in coll.find():
         content = remove_tags(job["summary"]).strip()
         job["notag"] = content
         coll.save(job)

def createIndex(coll):
    #coll =  jobColl
    print "collname=", coll.name
    indexdir = "index__"+coll.name
    removeHtml(coll)
    if not os.path.exists(indexdir):
        os.makedirs(indexdir)  
    ix = index.create_in(indexdir, schema)
    writer = ix.writer()
    for job in coll.find():  
        if job.has_key("job_title"):
            job["jobtitle"] = job["job_title"]
 #       print    job["_id"] , ">>" , job["jobtitle"].encode("GBK", "ignore")
       # print     job["notag"].encode("GBK", "ignore")
        writer.add_document(jobtitle= job["jobtitle"], jobid=job["_id"],
              content=job["notag"])
         
    writer.commit()

def search(indexdir, keyoword):
    ix = index.open_dir(indexdir)
    with ix.searcher() as searcher:
       query = QueryParser("content", ix.schema).parse(keyoword)
       print "query =", query 
   #    results = searcher.search(query, limit=20)
   #    results = searcher.search(query )   
      # results = searcher.search_page(query, pageno, pagelen=20)
       results = searcher.search(query, limit=None)  
     
       length = results.scored_length()     
       print "search length=", length
      
       ids = []
       for result in results:
        #   print result
           ids.append(result["jobid"])
       return ids
       
def searchColl(coll, keyoword):
    indexdir = "index__"+coll.name
    return search(indexdir, keyoword)
      
def createJobIndex():
    dbClient = DbClient('localhost', 27017, "jobaly")  
    collname = "job1000"
    coll = dbClient.getCollection(collname)
     
    createIndex(coll)
    
def test_search():
    results =  search("Java")
    i = 0
    for result in results:
        i+=1
        print i, ":" , result
        
    
if __name__ == '__main__':
    
  #  removeHtml()
    createJobIndex()
  #  test_search()