# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 20:34:21 2014

@author: dlmu__000
"""

import json

def dumpToText(listObj, fileName, lam):
     with open(fileName, "w") as f:
         for item in listObj:              
             line = lam(item) + "\n"
         #    print line.encode("GBK", "ignore")
             f.write(line.encode('utf8'))
         
def dumpToJson(listObj, fileName):
     with open(fileName, "w") as f:
         json.dump(listObj, f)
     
def dumpTwo(listObj, fileName , lam):
    txtFileName = fileName+".txt"
    jsonFileName = fileName+".json"
    dumpToText(listObj, txtFileName , lam)
    dumpToJson(listObj, jsonFileName)
    
def loadJson(data_set_name):     
     json_file = data_set_name+".json"
     with open(json_file, "r") as f :      
         return  json.load(f)