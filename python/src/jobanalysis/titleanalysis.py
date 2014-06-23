# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:14:13 2014

@author: dlmu__000
"""
import sys
sys.path.append("..")
import jobaly.utils
import json
import tokenfilter


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

def filterCat(titleList , catName):
    filterFile = "filters//"+catName+"_filter.txt"
    filterList = jobaly.utils.loadArrayFromFile(filterFile)  
    resultList, newleftList = tokenfilter.filterByContains(titleList, filterList )
    dumpTwo(resultList, "titles//"+catName) 
    return newleftList

def main():   
    
    titleList = json.loads(open('titles//titleList.json').read())
    # print type(titleList)
    devFilter = jobaly.utils.loadArrayFromFile("filters//dev_filter.txt")  
    resultList, leftList = tokenfilter.filterByContains(titleList, devFilter )
    dumpTwo(resultList, "titles//softeng")     
    
    leftList =   filterCat(leftList, "dba")
    leftList =   filterCat(leftList, "qa")
    leftList =   filterCat(leftList, "data")
    leftList =   filterCat(leftList, "programman")
    leftList =   filterCat(leftList, "productman")
    leftList =   filterCat(leftList, "support")
    
   
    dumpTwo(leftList, "titles//lefttitle")  
    
if __name__ == "__main__": 
    main()