# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 23:05:14 2014

@author: dlmu__000
"""
# such matcher how to handle repeat? 

class BaseMatcher:    
   
    def __init__(self):
        self.catch = []  
    
    def reset(self):
        self.catch = []    
        
    def match(self, tokens):
        return  -1
        
    def __call__(self, words):
        return self.match(words)
    
        
class TokenMatcher(BaseMatcher):
    
    def __init__(self, tokens):
        BaseMatcher.__init__(self)
        if type(tokens) is str:
            self.tokens = [tokens]
        elif type(tokens) is list:
            self.tokens = tokens
       
    def match(self, words):
        self.reset()
        if len(words) < len(self.tokens):
            return  -1
        
        i = 0 
        while i<len(self.tokens) and \
            self.tokens[i] == words[i]:
            self.catch.append(words[i])
            i += 1
        
        if i == len(self.tokens):
           return  i 
        else:
           return  -1
          
class SeqMatcher(BaseMatcher):
    
    def __init__(self, machers=None):
         BaseMatcher.__init__(self)
         if machers == None :
             self.machers = []
         elif type(machers) is list or \
             isinstance(machers, SeqMatcher ):
             self.machers = machers
         elif isinstance(machers, BaseMatcher ):
             self.machers = [machers]
                 
       
    def match(self, words):
        self.reset()
       
        j = 0  # index of matcher 
        i = 0
        while j<len(self.machers) and ( i != -1):
            macher = self.machers[j]
            i =  macher(words)
            if i != -1:
               self.catch.extend(macher.catch) 
               words = words[i:]
               j +=1
               
        if j == len(self.machers):
            return  len(self.catch)
        else:
            return  -1
                 

def findMatching( words, matcher):
    
    i = 0
    while i < len(words) :
        if matcher(words[i:]) != -1:
           return i
        else:
           i += 1
    return -1
    