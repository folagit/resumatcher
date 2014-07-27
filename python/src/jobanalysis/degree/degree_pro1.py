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
import operator



def preProcessFun(line):
    line =  re.sub (ur"\u2022|\u00b7|\uf09f|\uf0a7", "",line)
    line =  re.sub ("·", "",line, re.UNICODE) 
    line =  re.sub ("\*", "",line)
    line =  re.sub(ur"\u2019|\u2018", "\'", line)
  
    line =  re.sub(ur"\&", "and", line)
    line =  re.sub(ur"[B|b]achelor \'s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \'s", "masters", line)
    line =  re.sub(ur"[B|b]achelor \' s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \' s", "masters", line)
   
    line = line.strip()
    if line.find("-")==0 or line.find("\"")==0  \
        or line.find("\'")==0  or line.find("\,")==0  :
        line = line[1:].strip()
    return line

dumpLam1 = lambda x: x[0] + " | " + x[1]
dumpLam2 = lambda x: x[0] + " | " + str( x[1] ) + " | " + x[2]

def preProcess():
    max_length = 400
    data_set_name = "matching_degree_1"  
    target_set_name = "degree_1"     
        
    data_set_name = "matching_muldegree_3"  
    target_set_name = "degree_3"     
    
    data = datautils.loadJson(data_set_name)
    tokenMatch =  TokenMatcher("degree")
    newdata = []
    for item in data:
        if len (item[1] ) < 200 : 
            item.append ( preProcessFun(item[1]) )
            item[1] = len(item[2].split())
            newdata.append(item)
    newdata = sorted(newdata, key=operator.itemgetter(1) )
    datautils.dumpTwo(newdata, target_set_name, dumpLam2)    

def  beforeDegree():
    data_set_name = "degree_1"       
    data = datautils.loadJson(data_set_name)
    dict1 = {}
    for item in data:
        words = item[1].lower().split()
        i = findToken("degree", words)
        if ( i != -1 ) :
            if i == 0 :
                term = "__NO__"
            else: 
                term = words[i-1]
      #  print term.encode("GBK", "ignore")
        if dict1.has_key(term):
            dict1[term]+=1
        else :
            dict1[term]=1
      #  print term.encode("GBK", "ignore")
    datautils.printStatDict(dict1)
   
    
def labelDegree():
    # two letter word need compare orginal
    HS_LEVEL = ["High School Diploma", "High School"]    
    AS_LEVEL = ["AS"]
    BS_LEVEL = ["bachelors", "bachelor" ,"B.S.","BS","BA","BA/BS" ,"4-year","4-year", "four year" ]    
    MS_LEVEL = ["masters", "MS", "M.S."]
    PHD_LVEL = ["PhD", "Ph.D", "doctorate"]
    
    data_set_name = "degree_1"       
    data = datautils.loadJson(data_set_name)
    dict1 = {}
    for item in data:
        words = item[1].split()
        
    
    
 
def pipeLine():    
    data_set_name = "matching_degree_1"       
    data = datautils.loadJson(data_set_name)
   # preProcess(data)        
  
def main(): 
   preProcess()
 #  beforeDegree()
    
if __name__ == "__main__": 
    main() 