# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 16:26:26 2014

@author: dlmu__000
"""

import sys
sys.path.append("..")
from  data import datautils
from data.tokenfilter import *
import re
import operator

sys.path.append("../..")
from jobaly.fst.tokenre  import *

def removeSplash(line):
    slash_list = ["and/or", "PL/SQL"]  
    
    replace = True
    while replace:
        replace = False
        for word in line.split(): 
            if word.find("/") != -1 and len(word)>1:
                if  not ( word in slash_list ): 
                    print "*****removeSplash phrase is: ",  word                            
                    newword = re.sub("/", " / ", word)
                    line = re.sub(word, newword, line ) 
                    repalce = True
   
    return line

def preProcessFun(line):
    line =  re.sub (ur"\u2022|\u00b7|\uf09f|\uf0a7|\u0080|\u0099|\u00a2|\u0095|\u00d8|\u00bf|\u00c2|\u2219|\u20ac|\u2122", "",line)
    line =  re.sub ("·", "",line, re.UNICODE) 
    line = re.sub (ur"\u2013", "-", line)
    line =  re.sub ("\*", "",line)
    line =  re.sub(ur"\u2019|\u2018|\u00e2|\u0092|\u2020" , "\'", line)
    line = re.sub(ur"\u00ae", "", line)
    line =  re.sub(ur"\&", "and", line)
    line =  re.sub(ur"\/", " , ", line)
    line =  re.sub(ur"(|)", "", line)
    
    
    
    if line.find("/") != -1 :
         line = removeSplash(line)  

    line =  re.sub(ur"[B|b]achelor's", "bachelors", line)
    line =  re.sub(ur"[B|b]achelor \'s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \'s", "masters", line)
    line =  re.sub(ur"[B|b]achelor \' s", "bachelors", line)
    line =  re.sub(ur"[B|b]achelor s", "bachelors", line)
    line =  re.sub(ur"[M|m]aster \' s", "masters", line)    
    line =  re.sub(ur"[A|a]ssociate \' s", "associates", line)   
    line =  re.sub(ur"[A|a]ssociate \'s", "associates", line)   
    line =  re.sub(ur"Phd", "PhD", line)  
   
    line = line.strip()
    if line.find("-")==0 or line.find("\"")==0  \
        or line.find("\'")==0  or line.find("\,")==0  :
        line = line[1:].strip()
    return line

dumpLam1 = lambda x: x[0] + " | " + x[1]
dumpLam2 = lambda x: x[0] + " | " + str( x[1] ) + " | " + x[2]

def preProcess(data_set_name, target_set_name):
    
    max_length = 200
    data = datautils.loadJson(data_set_name)    
    newdata = []
    for item in data:
        if len (item[1] ) < max_length : 
            item.append ( preProcessFun(item[1]) )
            item[1] = len(item[2].split())
            newdata.append(item)
    newdata = sorted(newdata, key=operator.itemgetter(1) )
    datautils.dumpTwo(newdata, target_set_name, dumpLam2)    


def main():  
        
   data_set_name = "output\\matching_degree_1"  
   target_set_name = "output\\degree_1" 
   
   data_set_name = "output\\degree_raw"  
   target_set_name = "output\\degree_3"   
   
   data_set_name = "output\\degree_0610"  
   target_set_name = "output\\degree_after_0610"  
   
   preProcess(data_set_name, target_set_name)
 
if __name__ == "__main__": 
    main() 