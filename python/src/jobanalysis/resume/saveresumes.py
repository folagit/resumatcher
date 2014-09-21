# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 23:54:12 2014

@author: dlmu__000
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from  jobaly.pdf import pdftotxt
from jobaly.db.dbclient import DbClient



def scandir(path):
    dirs = os.listdir( path )
    pdffiles = []
    for filename in dirs:
     # print filename
      # print filename[-4:]
      if filename[-4:] == ".pdf" :
           pdffiles.append(filename)
            
    return pdffiles
    
def saveResumes(path, collection):
    pdffiles = scandir(path)
    for pfile in pdffiles:
        filename = path+pfile
     #   print filename
        lines = pdftotxt.pdftolines(filename)
        collection.save({"text":lines})

def main(): 
  path = "..\\..\\..\\..\\data\\resumes\\web\\"
 # scandir(path)
  
  srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
  resumeCollName = "web_resumes" 
  resumemodelCollName = resumeCollName+"_model"
  collection = srcBbClient.getCollection(resumeCollName)
  modelColl = srcBbClient.getCollection(resumemodelCollName)
  
  saveResumes(path, collection)
    
if __name__ == "__main__": 
    main()   