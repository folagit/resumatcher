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
import math
from pprint import pprint 
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
    
def getDistanceMatrix(sents, terms):
    n = len (terms)
    matrix = [ [ 1 for j in range(n) ] for i in range(n) ]
  #  print matrix
    for i in range(n):
        for j in range(i+1,n):
            term1 = terms[i]
            term2 = terms[j]
            dis = getDistanceInSents(sents, term1, term2)
            matrix[i][j]  = dis
            matrix[j][i]  = dis
            
    return matrix
    
def printDisMatrix(terms, matrix):
    from prettytable import PrettyTable
    terms.insert(0, " TERM " )    
    x = PrettyTable(terms)     
    x.padding_width = 1 # One space between column edges and contents (default)
    for i in range(len(terms)-1):
         row = matrix[i][:]
         row.insert(0, terms[i+1])
         x.add_row(row)
    print x
    
def getDisMatrixFromColletion(): 
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
        
     terms=["javascript", "jquery", "html", "css", "java", "jsp", "python", "ruby", "ror"  ]
    # terms=["java","jdbc","spring","hibernate","mysql","oracle"]
     matrix = getDistanceMatrix(docs, terms)   
     printDisMatrix(terms, matrix)   
     matrix_dump = json.dumps(matrix)
     print matrix_dump

sent1 = "dasf adf aaa df ewe bbb werew e ewrewre ewrwe ee ee".split()
sent2 = "dasf adf aaa df ewe bbb werew aaa e ewrewre ewrwe ee ee".split()
sent3 = "dasf adf aaa df ewe bbb werew aaa e ewrewre ewrwe ee ee aaa bbb".split()    
sent4 = "dasf adf aaa df ewe bd werew e ewrewre ewrwe ee ee".split()
sent5 = "aaa dasf adf bbb".split()

sents = [sent1, sent2, sent3, sent4, sent5]
    
def test_getMinDistance():        
    print  getMinDistance(sent4, "aaa", "bbb")
    
def test_getDistanceInSents():
    print  getDistanceInSents(sents, "aaa", "bbb")
    
def test_getDistanceMatrix():
    terms=["aaa","bbb" , "werew" , "ee" ]
    result = getDistanceMatrix(sents, terms)
  #  pprint(result)
    printDisMatrix(terms, result)
    


def main(): 
   # test_getDistanceMatrix()
   getDisMatrixFromColletion()
    
if __name__ == "__main__": 
    main()   
         
            
    