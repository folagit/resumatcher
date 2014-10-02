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
    terms = [x.split() for x in terms]
      
    for term in terms: 
       i = 0 ; find = 0
       while find != -1 :  
           find = findTokens( doc[i:],  term)
           if find != -1 :
               result.append(i+find)
               i += find+len(term)
               
       print " term= ", term, "--- result =", result 
    return sorted(result)


def getDistanceInsent(sent, terms1, terms2): 
    hasterm = False
    
    for term in terms1:
        find1 = sent.find(term)
        if  find1 != -1 :
            break
        
    for term in terms2:
        find2 = sent.find(term)
        if  find2 != -1 :
            break
            
    if ( find1 != 1 ) and ( find2 != -1 ) :
        mindis = math.abs(find1 - find2 )
        print "mindis = ", mindis
        return (mindis, True)
    elif ( find1 != 1 ) or ( find2 != -1 ) :
        return (-1, True ) 
    else : 
        return (-1, False ) 
   
        
def getDistanceInSents(doc, terms1, terms2):    
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
    
           
def getPairDistanceInColl(): 
     srcBbClient = DbClient('localhost', 27017, "jobaly_daily_test")
     collection = srcBbClient.getCollection("daily_job_webdev")
     
     docs = []
     for job in collection.find(): 
      #   print "\n\n\n======",job["_id"],"============================\n"
        jobDesc = JobDescParser.parseJobDesc(job)
        sents = jobDesc.listAllSentences() 
       
        doc =[]
        for sent in sents:
            tokens = [ token.lower() for token in word_tokenize(sent)]              
            doc.extend(tokens)      
        docs.append(doc)    
    
     owlfile = "..\\..\\jobaly\\ontology\\web_dev.owl"
     ontology = OntologyLib(owlfile)
     pairs = ontology.getSimilarityPairs()
     for p in pairs:
         ref1, ref2 =  p
         getPairDistance(ontology, ref1, ref2, docs)
       
     return 
     
def getPairDistance(ontology, ref1, ref2, docs):
     terms1 = [ x.split() for x in ontology.getTerms(ref1)]
     terms2 = [ x.split() for x in ontology.getTerms(ref2)]
     print "terms1=" , terms1
     print "terms2=" , terms2
     for doc in docs: 
         for sent in doc:
             pass

    
def test_findTokens():
    words = "bbbe ccc aaa dd ccc".split()
    result = findTokens( words, ["aaa"])
    print result
    
def test_findTerms():
    words = "aaa bbbe ccc aaa dd ccc dd".split()
    result = findTerms( words, ["aaa", "bbb", "dd ccc"])
    print result


def main():   
   # getPairDistance()
     test_findTerms()
   # test_findTokens()
    
if __name__ == "__main__": 
    main()   
         
            
    