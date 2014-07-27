# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:24:09 2014

@author: dlmu__000
"""

class JSentence():
    puncts = [".", ",", ";","?", "!", ":" ]
    tagDict = { "or": "OR", "and" : "AND" }    
    
    def __init__(self, words):
        self.words = words
        self._firstTag()
        
    def _firstTag(self):         
        self.tags = [None] * len(self.words)
        i = 0       
        while i < len(self.words):
            word = self.words[i]     
            if word in  JSentence.puncts :
                self.tags[i] = (  word , True )                
            elif JSentence.tagDict.has_key(word):
                self.tags[i] = ( JSentence.tagDict[word], True )
                
            i+=1
             
  
def test_sentence1():
    words = "I am ok or not , with you and me .".split()  
    
    sent = JSentence(words)
    print sent.tags
    
            
                
def main(): 
   test_sentence1()
 #  beforeDegree()
    
if __name__ == "__main__": 
    main() 