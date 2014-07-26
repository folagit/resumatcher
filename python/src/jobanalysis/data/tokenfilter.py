# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 22:25:07 2014

@author: dlmu__000
"""
import re
from nltk import word_tokenize, wordpunct_tokenize
    
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
     minIndex = len(string)+10
     for item in orList:
         i = string.find(item)
         if i != -1 and i+len(item) < minIndex:
             minIndex = i+len(item)
             
     if minIndex == len(string)+10:
         return -1
     else :
         return   minIndex
    

def contains(string, containStr):
    if ("," not in containStr) and ("|" not in containStr):
        return  string.find(containStr) != -1
    else:        
        seqList = containStr.split(",")
     #   print seqList
        for item in seqList:        
             i = orFind(string,item) 
             if i == -1 :
                 return False
             else :
                 string = string[i:]
         #        print string             
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

def test_contains():
  #   print contains("aabb","cc|aa")
  #   print contains("Front End Developer for a Hot Fashion Startup from Techstars", "Front End|Front")
  #   print contains("Java Developer- mid-level", "Java|Python|Ruby,Developer|Engineer|Architect|Development" )     
  #   print contains("Java Developer- mid-level", "Java|Python|Ruby,Developer" )     
      print contains( "Java/J2EE Developer", "Java|Python|Ruby,Developer" )   

def testTokenize():
    title = "Java Developer- mid-level"
    tokens = word_tokenize(title)    
    print tokens
    
    tokens =wordpunct_tokenize(title)
    print tokens

def main():   
    testTokenize() 
    
if __name__ == "__main__": 
    main()