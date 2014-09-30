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

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

from  webapp import dataHandler
import re
TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
indexdir = "index"
ix = create_in(indexdir, schema)
jobColl = dataHandler.jobCollection

def removeHtml():
    
     for job in jobColl.find():
         content = remove_tags(job["summary"]).strip()
         job["notag"] = content
         jobColl.save(job)

def createIndex(coll):
    
    writer = ix.writer()
    for job in coll.find():
        content = "d"
        writer.add_document(title=u"First document", path=u"/a",
              content=u"This is the first document we've added!")
         
    writer.commit()

def search(keyoword):
    with ix.searcher() as searcher:
      query = QueryParser("content", ix.schema).parse("first")
      results = searcher.search(query)
      print results[0]
      
def createJobIndex():
    coll = dataHandler.jobCollection
    createIndex(coll)
    
if __name__ == '__main__':
    
    removeHtml()