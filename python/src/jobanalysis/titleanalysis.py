# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:14:13 2014

@author: dlmu__000
"""

import jobaly.utils


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
 
def main(): 
    titleList = json.loads(open('titles//titleList.json').read())
    # print type(titleList)
    sdelist,leftlist = filterSDE(titleList)
    dumpTwo(sdelist, "titles//softeng")  
    dumpTwo(leftlist, "titles//lefttitle")  
    
if __name__ == "__main__": 
    main()