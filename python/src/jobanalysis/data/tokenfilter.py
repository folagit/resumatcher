# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 22:25:07 2014

@author: dlmu__000
"""

class BaseMatcher():
    
    def __init__(self, matchfun ):
        self._matchfun = matchfun
    
    def __call__(self, words):
        return self._matchfun(words)
        
    def __or__(self, other):
        def comb_fun(words):
        #    print "or or or "
            return self(words) or other(words)
        return  BaseMatcher(comb_fun)
        
    def __and__(self, other):
        def comb_fun(words):
        #    print "and and and"
            return self(words) and other(words)
        return  BaseMatcher(comb_fun)
        
    def __invert__(self):
        def comb_fun(words):
    #        print "not not not "
            return not self(words)  
        return  BaseMatcher(comb_fun)
        
class TokenMatcher(BaseMatcher):    
     def __init__(self, token  ):
        self._matchfun = tokenFind(token)

def tokenFind(token, lower=True):
    def fun(words):
        return tokenFind_fun(token, words, lower)
    return fun

def tokenFind_fun(token, words, lower=True):
    if lower :
        token = token.lower()
    return token in words
    
class TokensInMatcher(BaseMatcher):    
     def __init__(self, token  ):
        self._matchfun = tokenIn(token)

def tokenIn(tokens, lower=True):
    def fun(words):
        return tokensIn_fun(tokens, words, lower)
    return fun

def tokensIn_fun(tokens, words, lower=True):
    for token in tokens:
        if token in words: 
            return True
    return False

     
    
def termMatching(allSents,term):    
    matchingSents =[]
    for (jid, sent) in allSents:
        tokens = [ token.lower() for token in word_tokenize(sent)]
        if term in tokens : 
            matchingSents.append((jid, sent))
    return  matchingSents 

