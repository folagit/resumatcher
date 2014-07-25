# -*- coding: utf-8 -*-
"""
Created on Tue Jul 22 17:11:11 2014

@author: dlmu__000
"""
# "dsff|sdf|sfs"
def listOrIn(tokens, sent, simple = True):
    for token in tokens:
        index = sent.find(token)
        if  index  != -1 :
            if simple: 
                return True
            else: 
                return (True, token, index)
    if simple:    
        return False
    else:
        return (True, None, -1)
        
# "(AC|BC) is (ed|df)"
def sequenceAllIn(tokens, sent):     
    for item in tokens:        
         i = sent.find(item) 
         if i == -1 :
             return False
         else :
             sent = sent[i+len(item):]
              #   print string             
    return True     
    
def test_listOrIn():
    
    sent = "dsf dsfe dsfee oee"
    tokens = ["da"]
    tokens = ["da", "sfe"]
    print listOrIn(tokens, sent)    
    
def test_sequenceAllIn():
    
    sent = "dsf dsfe dsfee oee"
    tokens = ["da"]
    tokens = ["da", "sfe"]
    tokens = ["fe", "sfe"]
    print sequenceAllIn(tokens, sent)   

def main():
   test_sequenceAllIn()
    

if __name__ == "__main__": 
    main()
            