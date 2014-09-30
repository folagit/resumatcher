# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 18:04:51 2014

@author: dlmu__000
"""

from whoosh.index import create_in
from whoosh.fields import *
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
indexdir = "."
ix = create_in(indexdir, schema)
writer = ix.writer()
writer.add_document(title=u"First document", path=u"/a",
      content=u"This is the first document we've added!")
writer.add_document(title=u"Second document", path=u"/b",
      content=u"The second one is even more interesting!")
writer.commit()
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
  query = QueryParser("content", ix.schema).parse("first")
  results = searcher.search(query)
  print results[0]