# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:30:33 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:04:51 2014

@author: dlmu__000
"""

from whoosh import index 
from whoosh.fields import *
from whoosh.qparser import QueryParser

from  webapp import dataHandler
import re
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub(' ', text)

schema = Schema(jobtitle=TEXT(stored=False), jobid=ID(stored=True), content=TEXT)
indexdir = "index"

#searcher = myindex.searcher()
jobColl = dataHandler.jobCollection

def removeHtml():
    
     for job in jobColl.find():
         content = remove_tags(job["summary"]).strip()
         job["notag"] = content
         jobColl.save(job)

def createIndex():
    coll =  jobColl
    ix = index.create_in(indexdir, schema)
    writer = ix.writer()
    for job in coll.find():  
        
 #       print    job["_id"] , ">>" , job["jobtitle"].encode("GBK", "ignore")
       # print     job["notag"].encode("GBK", "ignore")
        writer.add_document(jobtitle= job["jobtitle"], jobid=job["_id"],
              content=job["notag"])
         
    writer.commit()

def search(keyoword):
    ix = index.open_dir(indexdir)
    with ix.searcher() as searcher:
       query = QueryParser("content", ix.schema).parse(keyoword)
       print "query =", query 
       results = searcher.search(query, limit=20)
       ids = []
       for result in results:
        #   print result
           ids.append(result["jobid"])
       return ids
      
def createJobIndex():
    coll = dataHandler.jobCollection
    createIndex(coll)
    
def test_search():
    results =  search("Java")
    i = 0
    for result in results:
        i+=1
        print i, ":" , result
        
    
if __name__ == '__main__':
    
  #  removeHtml()
  # createIndex()
    test_search()