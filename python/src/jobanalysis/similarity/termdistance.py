# -*- coding: utf-8 -*-
"""
Created on Thu Sep 04 14:27:10 2014

@author: dlmu__000
"""

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
    
def test_getMinDistance():
    
    sent1 = "dasf adf aaa df ewe bbb werew e ewrewre ewrwe ee ee".split()
    sent2 = "dasf adf aaa df ewe bbb werew aaa e ewrewre ewrwe ee ee".split()
    sent3 = "dasf adf aaa df ewe bbb werew aaa e ewrewre ewrwe ee ee aaa bbb".split()    
    sent4 = "dasf adf aaa df ewe bd werew e ewrewre ewrwe ee ee".split()
    sent5 = "aaa dasf adf bbb".split()
        
    print  getMinDistance(sent4, "aaa", "bbb")
    

def main(): 
   test_getMinDistance()
    
if __name__ == "__main__": 
    main()   
         
            
    