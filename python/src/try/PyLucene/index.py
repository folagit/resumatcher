# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 00:19:48 2014

@author: dlmu__000
"""

import os,sys,glob
import lucene

from lucene import SimpleFSDirectory, System, File, Document, Field, \
StandardAnalyzer, IndexWriter, Version

"""
Example of Indexing with PyLucene 3.0
 """

def luceneIndexer(docdir,indir):

         """

         IndexDocuments from a directory

         """

         lucene.initVM()

         DIRTOINDEX= docdir

         INDEXIDR= indir

         indexdir= SimpleFSDirectory(File(INDEXIDR))

         analyzer= StandardAnalyzer(Version.LUCENE_30)

         index_writer= IndexWriter(indexdir,analyzer,True,\

         IndexWriter.MaxFieldLength(512))

         for tfile in glob.glob(os.path.join(DIRTOINDEX,'*.txt')):

                   print"Indexing: ", tfile

                   document= Document()

                   content= open(tfile,'r').read()

                   document.add(Field("text",content,Field.Store.YES,\

                            Field.Index.ANALYZED))

                   index_writer.addDocument(document)

                   print"Done: ", tfile

         index_writer.optimize()

         print index_writer.numDocs()

         index_writer.close()
         
if __name__ == "__main__":
      docdir = "..\\..\\..\\data\\resumes\\web"
      indir = "."
      luceneIndexer(docdir,indir)