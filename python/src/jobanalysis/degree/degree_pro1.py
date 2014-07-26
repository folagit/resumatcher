# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 20:31:27 2014

@author: dlmu__000

"""
import sys
sys.path.append("..")
from  data import datautils
from data.tokenfilter import *
import re

dumpLam = lambda x: x[0] + " | " + x[1]

def preProcessFun(line):
    line =  re.sub (ur"\u2022|\u00b7|\uf09f", "",line)
    line =  re.sub ("·", "",line, re.UNICODE) 
    line =  re.sub ("\*", "",line)
    line =  re.sub(ur"\u2019", "\'", line)
    line = line.strip()
    if line.find("-") == 0:
        line = line[1:].strip()
    return line

def preProcess():
    data_set_name = "matching_degree_1"       
    data = datautils.loadJson(data_set_name)
    tokenMatch =  TokenMatcher("degree")
    for item in data:
        item[1] = preProcessFun(item[1])
    datautils.dumpTwo(data, "degree_1", dumpLam)    
 
def pipeLine():    
    data_set_name = "matching_degree_1"       
    data = datautils.loadJson(data_set_name)
   # preProcess(data)        
  
def main(): 

   preProcess()
    
if __name__ == "__main__": 
    main() 