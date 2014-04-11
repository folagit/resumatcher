# -*- coding: utf-8 -*-
"""
Created on Sun Apr 06 23:13:33 2014

@author: dlmu__000
"""
from dbclient import DbClient 
import re



def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def clearReturn(txt):
     return re.sub("\\\n\-|\\\n", " ",txt)    
    
def clearSymbol(token):
     token = re.sub('\.|\,|\-|\)|\(|\:|\-|\_|\?|\!|\>|\<|\"|\[|\]|\~|\'|\*|\=|\{|\}|\\\n', '', token)
     return  token     
    
def processText(txt):
    txt = striphtml(txt)
  #  txt = clearSymbol(txt)
    txt = clearReturn(txt)
    return txt
    
def processPage(collection, page,pageNo):
     
     i = 0
     for jobitem in page:
         jobitem["content"] = None
         content =  processText(jobitem["summary"])         
         if  content == None or len(content ) == 0:
             print jobitem["_id"]
             return 
         jobitem["content"] = content
         collection.save(jobitem)
         i+=1
                 
     print "%d jobs has been saved for page %d " %(i, pageNo)
   
    
def main():
     
     collectionName = "jobinfo_se_top_corps"     
     dbClient = DbClient('localhost', 27017, "jobaly")
     collection = dbClient.getCollection(collectionName)
    
     pageSize = 100 
     pageNo = 1
     has_more = True
     pageNum = 10000
     find_sort = None
     find_spec=None
     while has_more and pageNo <= pageNum :
        page = dbClient.getPage(collection, find_spec,find_sort, pageSize, pageNo)    
        processPage(collection, page,pageNo)        
        pageNo+=1 
        count =  page.count(with_limit_and_skip = True)
     #   print "count=",count
        if ( count < pageSize ) :
            has_more = False
         
    
if __name__ == "__main__": 
    main()