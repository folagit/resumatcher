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

def getMinDistance(tokens, term1, term2):
    list1 = []
    last = None
    mindis = len(tokens)
    hasterm = False
    for i in range(len(tokens)): 
        if  term1 == tokens[i] or term2 == tokens[i]:  
            hasterm = True
            node = (i, tokens[i] )
            list1.append( (i, tokens[i] ) )             
            if last is not None:
                if last[1] != node[1] and i-last[0] < mindis :
                    mindis = i-last[0]
                    if mindis == 1:
                        break
            last = node
            
    if mindis == len(tokens):
        return (-1, hasterm ) 
    else :
        return ( mindis, hasterm ) 
        
def getDistanceInSents(sents, term1, term2):    
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
            sent = " "+sent+" "               
            doc.extend(sent)        
        docs.append(doc)    
    
     owlfile = "..\\..\\jobaly\\ontology\\web_dev.owl"
     ontology = OntologyLib(owlfile)
     pairs = ontology.getSimilarityPairs()
     for p in pairs:
         ref1, ref2 =  p
         getPairDistance(ontology, ref1, ref2, docs)
       
     return 
     
def getPairDistance(ontology, ref1, ref2, docs):
     terms1 = ontology.getTerms(ref1)
     terms2 = ontology.getTerms(ref2)
   
     matrix = getDistanceMatrix(docs, terms)   
     printDisMatrix(terms, matrix)   
     matrix_dump = json.dumps(matrix)
     print matrix_dump


def main():   
    getPairDistance()
    
if __name__ == "__main__": 
    main()   
         
            
    