# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 21:33:09 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from jobaly.db.dbclient import DbClient 
from jobanalysis.resume import resumeparser 
from jobanalysis.similarity.modelsimilarity import ModelSimilarity
 
import re

def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]',' ', text)

def getIndeedRank(dbname, collName):
      
    dbClient = DbClient('localhost', 27017, dbname)
    jobCollection = dbClient.getCollection(collName)
    i=1
    
    for job in jobCollection.find().sort("pos",1):        
         print job["_id"], job["pos"]
         if i==20 :
             break
         else:
             i+=1
    print "- - - - - - -"    
    i=1
    for job in jobCollection.find().sort("pos",1):        
         print job["_id"]
         if i==20 :
             break
         else:
             i+=1
         
def getOntology(resumefile, dbname, modelCollName):
  dbClient = DbClient('localhost', 27017, dbname)
  modelColl = dbClient.getCollection(modelCollName)  
  
  with open(resumefile, 'r') as content_file:
        content = content_file.read()
        content = remove_non_ascii_2(content) 
  resumeModel = resumeparser.parseResumeText(content)
 # print     resumeModel                          
  similarity = ModelSimilarity()   
  result = similarity.match_jobColl(resumeModel , modelColl  )
  n=1    
  for key, value in result[:20]:      
      print n, key, value
      n = n+1
  print "- - - - - - -"     
  for key, value in result[:20]:      
      print key 

def main():
     dbname = "jobaly"       
     keyword = "java"     
     resumefile = keyword + "_resume.txt"
     name = keyword.split()[0]
     jobCollectionName = "keyword_info_"+name
     modelCollName = jobCollectionName+"_model"
     print "------- indeed rank ----------" 
     getIndeedRank(dbname, jobCollectionName )     
    
     print "\n\n------- ontology rank ----------"
     getOntology(resumefile, dbname,  modelCollName)
      
if __name__ == "__main__": 
    main() 
   
 