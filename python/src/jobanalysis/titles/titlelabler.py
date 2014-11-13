# -*- coding: utf-8 -*-
"""
Created on Wed Nov 12 23:13:46 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from data.labeler import Labeler

def addLabels(labelDict, items, label):
    for item in items:
        labelDict[item] = label

def createLabelDict():
    labelDict = { "or": "OR", "OR": "OR", "and" : "AND" ,  "in": "IN" , "In":"IN" , \
           "of" : "OF", "and/or" : "AND_OR", "from" :"FROM" , "with":"WITH" , \
           "at":"AT" ,"about":"ABOUT" , "for" : "FOR" ,"as":"AS" }
        
    BE = ["Be","be", "is", "are", "was", "were", "am"]    
    DT = ["a", "A", "an", "An", "The", "the"]  
    DIGIT = ['one', "two", "three", "four", "five", "seven", "eight", "night", "ten" ]
    YEAR = ["year", "years", "yr"]
    
    addLabels(labelDict, BE, "BE" )  
    addLabels(labelDict, DT, "DT" )  
    addLabels(labelDict, DIGIT, "DIGIT" )  
    addLabels(labelDict, YEAR, "YEAR" )
    
  #  addDegreeLabel(labelDict)
  #  addMajorLabels(labelDict)
  #  addOtherLabels(labelDict)
    
    addDegreeLabel(labelDict)
    
    return labelDict
    
def addDegreeLabel(labelDict):
    
    ENG_ROLE=["Intern","Engineer","Architect","Development","Developer",
       "Programmer","dev","Computer Programmer","lead","CONSULTANT","Eng."]
        
      
    PRO_LANG = ["java", "c++", "python", ".net", "javascript" ]

    DEV_DOMAIN = ["web", "mobile"]    
    
    dba_terms=["Oracle","SQL Server","DB2","MySQL","DBA"]
    dba_roles=["Intern","DBA","Administrator","Architect","admin","Manager"]
    
    dba_terms=["Oracle","SQL Server","DB2","MySQL","DBA"]
    dba_roles=["Consultant","Intern","DBA","Administrator","Architect","admin","Manager"]
    
    qa_terms=["QA","Software Quality","Software","Test","Quality Assurance"]
    qa_roles=["Consultant","Intern","QA","Engineer","Manager","Lead","Tester","Technician","testing"]
                             
    data_terms=["Data"]
    data_roles=["Consultant","Intern","Scientist","Architect","Analytics","Engineer","Analyst","Anaylt"]
    
    programman_terms=["Program"]
    programman_roles=["Intern","Manager"]
    
    productman_terms=["Product Manager"]
    productman_roles=["Intern","Product Manager"]
    
    projectman_terms=["Project Manager"]
    projectman_roles=["Intern","Project Manager"]
    
    support_terms=["Cloud","IT","Software","System","Network","Production","Product","Linux","UNIX","Application","Support Engineer","Mainframe"]
    support_roles=["Intern","Support","Administration","Administrator","Support","Support Engineer","admin"]
    
    DevOps_terms=["DevOps","Dev/Ops", "Dev Ops"]
    DevOps_roles=["Intern","Engineer","Manager"]
    
    UI_terms=["UI"]
    UI_roles=["Intern","Designer","Engineer"]
    
    UE_terms=["User Experience","UX"]
    UE_roles=["Intern","Designer","Developer"]


    addLabels(labelDict, ENG_ROLE, "ENG_ROLE" )  
    addLabels(labelDict, PRO_LANG, "PRO_LANG" )  
    addLabels(labelDict, DEV_DOMAIN, "DEV_DOMAIN" ) 
    
          
   
 
def addOtherLabels(labelDict):
    MAJOR_DEGREE = ["MBA", "BSCS", "BSEE", "MSCS", "MSEE", "MSCE","MPH" ]
    addLabels(labelDict, MAJOR_DEGREE, "MAJOR_DEGREE" )
    
    
    
def createOntoDict():
    ontoDict = {}
    ROLE_NAME = [ "ENG_ROLE" ]
    ROLE_PRE  = [ "PRO_LANG" , "DEV_DOMAIN"]
   
    addLabels(ontoDict, ROLE_NAME, "ROLE_NAME" ) 
    addLabels(ontoDict, ROLE_PRE, "ROLE_PRE" ) 
    
    return ontoDict
    
def createTitleLabeler():
    labelDict = createLabelDict()   
    ontoDict = createOntoDict()
    labeler = Labeler(labelDict,ontoDict)
    return labeler  