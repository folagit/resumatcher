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
        self._matchfun = tokensIn(token)

def tokensIn(tokens, lower=True):
    def fun(words):
        return tokensIn_fun(tokens, words, lower)
    return fun

def tokensIn_fun(tokens, words, lower=True):
    for token in tokens:
        if  lower :
            token = token.lower()
        if token in words: 
            return True
    return False



def findToken(token, words, lower=True):
    if  lower :
        token = token.lower()
    i = 0
    while i < len(words):
        if token == words[i]:
            return i
        else :
            i+=1
    return -1
    
def findTokenSquence(tokens, _words, scope=None , lower=True):
    if scope is None :
        scope = (0, len(_words))
    
    
    start =  scope[0]
    word_len = scope[1]
    j  = 0
    l1  = len(tokens) 
    
    if word_len < l1 :
        return -1 
       
 #   print word_len, l1 
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
    
def termMatching(allSents,term):    
    matchingSents =[]
    for (jid, sent) in allSents:
        tokens = [ token.lower() for token in word_tokenize(sent)]
        if term in tokens : 
            matchingSents.append((jid, sent))
    return  matchingSents 

