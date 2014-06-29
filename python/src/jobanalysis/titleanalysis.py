# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:14:13 2014

@author: dlmu__000
"""
import sys
sys.path.append("..")
import jobaly.utils
import json
import stringfilter

 
dev_terms=jobaly.utils.loadArrayFromFile("filters/devterms.txt")
dev_roles=["Intern","Engineer","Architect","Development","Developer",
       "Programmer","dev","Computer Programmer","lead","CONSULTANT","Eng."]

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


def dumpToText(listObj, fileName):
     with open(fileName, "w") as f:
         for item in listObj:              
             line = item["_id"] + ":" + str(item["number"]) + "\n"
         #    print line.encode("GBK", "ignore")
             f.write(line.encode('utf8'))
         
def dumpToJson(listObj, fileName):
     with open(fileName, "w") as f:
         json.dump(listObj, f)
     
def dumpTwo(listObj, fileName):
    txtFileName = fileName+".txt"
    jsonFileName = fileName+".json"
    dumpToText(listObj, txtFileName)
    dumpToJson(listObj, jsonFileName)

def filterCatFile(titleList , catName):
    filterFile = "filters//"+catName+"_filter.txt"
    filterList = jobaly.utils.loadArrayFromFile(filterFile)  
    resultList, newleftList = stringfilter.filterByContains(titleList, filterList )
    dumpTwo(resultList, "titles//"+catName) 
    return newleftList
    
def filterCat(titleList , catName): 
    termList=[]
    rolesList = []  
    _g = globals()
    if _g.has_key(catName+"_terms"):        
        termList = _g[catName+"_terms"]
        if _g.has_key(catName+"_roles") :
            rolesList = _g[catName+"_roles"]

    if   len(termList) == 0 or  len(rolesList) == 0 :
        sys.stderr.write("no term or role list of: "+ catName+" ignore it!\n\n")
        return titleList
    
    resultList, newleftList = filterByContainLists(titleList, [termList, rolesList] )
    dumpTwo(resultList, "titles//"+catName) 
    return newleftList

def filterByContainLists(titleList, lists):
    resultList=[]
    leftList=[]    
    
    for item in titleList:
        #  print item["_id"].encode("GBK", "ignore")
        if  stringfilter.containAllList( item["_id"].lower(), lists ) :
            print item["_id"].encode("GBK", "ignore")
            resultList.append(item)
        else :
            leftList.append(item)
            
    return ( resultList, leftList )
    
def filterCats(titleList, catList):
    leftList = titleList
    for item in catList:
        leftList = filterCat(leftList, item)
    return leftList
def main():   
    
    titleList = json.loads(open('titles//titleList.json').read())
    # print type(titleList)   
    
    resultList, leftList = filterByContainLists(titleList, [dev_terms, dev_roles] )
         
    catList = ["dev","dba", "qa", "data", "programman", 
               "productman", "support",  "DevOps", "UI", "UE"]
    leftList = filterCats(titleList, catList)    
    dumpTwo(leftList, "titles//lefttitle")  
    
if __name__ == "__main__": 
    main()