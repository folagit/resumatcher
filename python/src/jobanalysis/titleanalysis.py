# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:14:13 2014

@author: dlmu__000
"""
import sys
sys.path.append("..")
import jobaly.utils
import re
import json


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
    
def orContains(string, containList):
    
    for item in containList:
        item = item.lower()         
        if contains(string,item) :
                return True         
    return False
    
def seqContains(string, containList):
     
    for item in containList:        
         i = string.find(item) 
         if i == -1 :
             return False
         else :
             string = string[i+len(item):]
              #   print string
             
    return True   
    
def orFind(string, containStr):
     orList = containStr.split("|")   
     minIndex = len(string)
     for item in orList:
         i = string.find(item)
         if i != -1 and i < minIndex:
             minIndex = i
             
     if minIndex == len(string):
         return -1
     else :
         return   minIndex
    

def contains(string, containStr):
    if ("," not in containStr) and ("|" not in containStr):
        return  containStr in string 
    elif  "," in containStr:
        seqList = containStr.split(",")
        for item in seqList:        
             i = orFind(string,item) 
             if i == -1 :
                 return False
             else :
                 string = string[i+len(item):]
                  #   print string
             
        return True   
    
    
def filterByContains(titleList, containList):
    resultList=[]
    leftList=[]    
    
    for item in titleList:
        #  print item["_id"].encode("GBK", "ignore")
        if  orContains( item["_id"].lower(), containList ) :
            print item["_id"].encode("GBK", "ignore")
            resultList.append(item)
        else :
            leftList.append(item)
            
    return ( resultList, leftList )
    
def filterByRegex(titleList):
    resultList=[]
    leftList=[]
    pattern = re.compile('(.*Software Engineer)|(.*Software Developer)',re.IGNORECASE)
    
    for item in titleList:
        #  print item["_id"].encode("GBK", "ignore")
        if  pattern.match( item["_id"] ) :
            print item["_id"].encode("GBK", "ignore")
            resultList.append(item)
        else :
            leftList.append(item)
            
    return ( resultList, leftList )

def filterSDE(titleList ):
    sedlist = []
    leftlist = []
    for item in titleList:
        #  print item["_id"].encode("GBK", "ignore")
        if  item["_id"].find("Software Engineer")!=-1 or \
            item["_id"].find("Software Developer")!=-1  :
            print item["_id"].encode("GBK", "ignore")
            sedlist.append(item)
        else :
            leftlist.append(item)
    
    return (sedlist, leftlist )
    
def test_orFind():
    print "result =" , str(orFind("aaeer ew", "ee|aa"))
    print "result =" , str(orFind("saaeer ew", "ee|aa"))
    print "result =" , str(orFind("saeder ew", "ee|aa|ewr"))
    print "result =" , str(orFind("saeder ew", "ee|aa|e"))
    print "result =" , str(orFind("saeder ew", "eewe"))
    print "result =" , str(orFind("saeder ew", "e"))
  
def test_seqContains():
    
    print "result =" , str(seqContains("aaaa  bb", ["bb", "CC"]))
    print "result =" , str(seqContains("aaaa  bb CC", ["bb", "CC"]))
    print "result =" , str(seqContains("123456bb CC", ["1","34", "CC"]))
 
def main():   
    
    titleList = json.loads(open('titles//titleList.json').read())
    # print type(titleList)
    devFilter = jobaly.utils.loadArrayFromFile("devfilter.txt")  
    resultList, leftList = filterByContains(titleList, devFilter )
    dumpTwo(resultList, "titles//softeng")  
    dumpTwo(leftList, "titles//lefttitle")  
    
if __name__ == "__main__": 
    main()