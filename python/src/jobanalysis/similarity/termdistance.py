# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 14:27:10 2014

@author: dlmu__000
"""

import math
from pprint import pprint 

def getMinDistance(tokens, term1, term2):
    list1 = []
    last = None
    mindis = len(tokens)
    for i in range(len(tokens)): 
        if  term1 == tokens[i] or term2 == tokens[i]:   
            node = (i, tokens[i] )
            list1.append( (i, tokens[i] ) )             
            if last is not None:
                if last[1] != node[1] and i-last[0] < mindis :
                    mindis = i-last[0]
            last = node
            
    if mindis == len(tokens):
        return -1
    else :
        return mindis
        
def getDistanceInSents(sents, term1, term2):
    result = []
    for sent in sents: 
        dis = getMinDistance(sent, term1, term2)
        if dis != -1 :
            result.append(dis)
    factor1 = float (len(result)) /len(sents)
    logdis = [   math.log(x+1,2) for x in result ]
    factor2 = sum(logdis)/len(result)
    print term1, term2, factor1, logdis, factor2, factor1 / factor2
    return factor1 / factor2
    
def getDistanceMatrix(sents, terms):
    n = len (terms)
    matrix = [ [ 1 for j in range(n) ] for i in range(n) ]
    print matrix
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
   test_getDistanceMatrix()
    
if __name__ == "__main__": 
    main()   
         
            
    