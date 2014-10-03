# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 14:27:10 2014

@author: dlmu__000
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from jobdescparser import JobDescParser
from nltk.tokenize import word_tokenize
from jobaly.db.dbclient import DbClient
from jobaly.ontology.ontologylib import OntologyLib
import math
import json

def findTokens( _words, tokens, scope=None, lower=True):
    if scope is None :
        scope = (0, len(_words))    
    
    start =  scope[0]
    word_len = scope[1]
    j  = 0
    l1  = len(tokens) 
    
    if word_len < l1 :
        return -1 
    
    if len(tokens) == 1 and len(tokens[0]) < 4 :
        words =  _words         
    else :
        if  lower :
            words = [word.lower() for word in _words]
        else :
            words =  _words
        
    i = start
    while i < start + word_len:
        i1 = i
        j = 0
        while j < l1 and i1 < start + word_len and tokens[j] == words[i1] :
             j+=1
             i1+=1
        if j == l1 :
            return i
        elif i1 == start + word_len :
            return -1
        else:
            i+=1            
            
    return -1

def findTerms(doc, terms):
    result = []
    i = 0
    find = 0
#    terms = [x.split() for x in terms]
      
    for term in terms: 
       i = 0 ; find = 0
       while find != -1 :  
           find = findTokens( doc[i:],  term)
           if find != -1 :
               result.append(i+find)
               i += find+len(term)
               
   #    print " term= ", term, "--- result =", result 
    return sorted(result)


def getMinDistance(find1, find2):
    
    len1 = len(find1)
    len2 = len(find2)
    if len1 == 0 and len2 == 0:
        return (-1, False ) 
    elif len1 == 0 or len2 == 0:
        return (-1, True ) 
    
    mindis = 99999
    
    for i in find1:
        for j in find2:
            dis =  abs(i-j)
            if mindis< dis:
                mindis = dis
            
    return (mindis, True)
   
        
def getDistanceInSents(sents, terms1, terms2):    
    result = []
    total = 0 
    for sent in sents: 
        dis, hasterm = getMinDistance(sent, term1, term2)
     #   print dis, hasterm
        if hasterm :
            total+=1
        if dis != -1 :
            result.append(dis)
    if len(result) == 0 : 
        return 0
 #   print len(result),  total
    factor1 = float (len(result)) / total
  #  logdis = [   math.log(x+1,2) for x in result ]
    logdis = [   math.log(x+1,2) for x in result ]
    factor2 = sum(logdis)/len(result)
  #  print term1, term2, factor1, logdis, factor2, factor1 / factor2
    result = round(factor1 / factor2, 4 )
  #  print term1, term2, factor1, factor2, result    
    return result
    
def createDocs():
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     collection = srcBbClient.getCollection("daily_job_webdev")
     maxnum =99999
     docs = []
     i= 0
     for job in collection.find(): 
        i+=1
        if i == maxnum: 
             break
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
       
        doc =[]
        for sent in sents:
            tokens = [ token.lower() for token in word_tokenize(sent)]              
            doc.extend(tokens)      
        docs.append(doc)   
    
     return docs
    
           
def getPairDistanceInColl(): 
     
     docs = createDocs()
     owlfile = "..\\..\\jobaly\\ontology\\web_dev.owl"
     ontology = OntologyLib(owlfile)
     pairs = ontology.getSimilarityPairs()
     pairdict = {}
     for p in pairs:
         ref1, ref2 =  p
         name1 = ref1.rsplit('#')[-1]    
         name2 = ref2.rsplit('#')[-1]   
         
         value = getPairDistance(ontology, ref1, ref2, docs)
         pairdict[(name1, name2)] = value
       
     return pairdict
     
def getPairDistance(ontology, ref1, ref2, docs):
     terms1 = [ x.lower().split() for x in ontology.getTerms(ref1)]
     terms2 = [ x.lower().split() for x in ontology.getTerms(ref2)]
   #  print "terms1=" , terms1
   #  print "terms2=" , terms2
     total = 0
     result = []
     for doc in docs: 
   #     print doc
        find1 = findTerms(doc, terms1)
        find2 = findTerms(doc, terms2)
   #     print 'find1=',find1
   #     print 'find2=',find2
        dis, hasterm = getMinDistance(find1,find2)        
  #      print dis, hasterm
        if hasterm :
            total+=1
        if dis != -1 :
            result.append(dis)
     if len(result) == 0 : 
        return 0
 #   print len(result),  total
     factor1 = float (len(result)) / total
  #  logdis = [   math.log(x+1,2) for x in result ]
     logdis = [   math.log(x+1,2) for x in result ]
     factor2 = sum(logdis)/len(result)
  #  print term1, term2, factor1, logdis, factor2, factor1 / factor2
     value = round(factor1 / factor2, 4 )
  #  print term1, term2, factor1, factor2, result  
   #  print "value=",value
     return value
     
def dumpPairValues():
    pairdict=  getPairDistanceInColl()    
    result = []
    for key ,value in pairdict.items():
        term1, term2 = key
        result.append( [ term1, term2, value] )   
        if value > 0 :
            print term1, term2, value
        
    with open('pairvalue.txt', 'w') as outfile:
       json.dump(result, outfile)
    
def test_findTokens():
    words = "bbbe ccc aaa dd ccc".split()
    result = findTokens( words, ["aaa"])
    print result
    
def test_findTerms():
    words = "aaa bbbe ccc aaa dd ccc dd".split()
    result = findTerms( words, ["aaa", "bbb", "dd ccc"])
    print result

def test_getPairDistanceInColl():
    
    pairdict = getPairDistanceInColl()
    for pair, value in pairdict.items():
        print pair, "-->>", value
        
def test_getPairDistance():
     docs = createDocs()
     owlfile = "..\\..\\jobaly\\ontology\\web_dev.owl"
     ontology = OntologyLib(owlfile)
     
     ref1 = ontology.toURIRef("HTML")
     ref2 = ontology.toURIRef("CSS")
     su = ontology.getSuperClass(ref1)
     for c in su:
         print c
         
     su = ontology.getSuperClass(ref2)
     for c in su:
         print c
         
     name1 = ref1.rsplit('#')[-1]    
     name2 = ref2.rsplit('#')[-1]   
     
     value = getPairDistance(ontology, ref1, ref2, docs)
     print "dd---" ,value    
    

def main():   
   # getPairDistance()
   #  test_findTerms()
   # test_findTokens()
   #test_getPairDistanceInColl()
   dumpPairValues()
 #  test_getPairDistance()
    
if __name__ == "__main__": 
    main()   
         
            
    