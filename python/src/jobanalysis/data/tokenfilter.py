# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 22:25:07 2014

@author: dlmu__000
"""

def tokenFind(token, lower=True):
    def fun(words):
        return tokenFind_fun(token, words, lower)
    return fun

def tokenFind_fun(token, words, lower=True):
    if lower :
        token = token.lower()
    return token in words

def termsMatching(allSents,terms):
    matchingSents =[]
    for (jid, sent) in allSents:
        tokens = [ token.lower() for token in word_tokenize(sent)]
        for term in  terms:      
            if term in tokens : 
                matchingSents.append((jid, sent))
                break
    return  matchingSents      
    
def termMatching(allSents,term):    
    matchingSents =[]
    for (jid, sent) in allSents:
        tokens = [ token.lower() for token in word_tokenize(sent)]
        if term in tokens : 
            matchingSents.append((jid, sent))
    return  matchingSents 


def test_tokenMatch():
    sent = "You can also install Spyder from its zip source package" 
    words = sent.split()
    print words
    token = "also"
    print tokenFind_fun(token, words)
    
    g = lambda x: tokenFind_fun( token ,x )
    print g(words)
    
    matchFun = tokenFind("install")
    print "install:" , matchFun(words)
    
    matchFun = tokenFind("insta")
    print "insta:" , matchFun(words)
   

def test_comb():
    sent = "You can also install Spyder from its zip source package" 
    words = sent.split()
    matchFun1 = tokenFind("install")
    matchFun2 = tokenFind("also")
    matchFun3 = tokenFind("als")
    comb1 = lambda x : matchFun1( x ) and matchFun2( x )
    comb2 = lambda x : matchFun1( x ) and matchFun3( x )
    comb3 = lambda x : matchFun1( x ) or matchFun3( x )
      
    print "comb1" , comb1(words)    
    print "comb2" , comb2(words)
    print "comb3" , comb3(words)
    
    
def main():   
  #  test_tokenMatch() 
    test_comb()
    
if __name__ == "__main__": 
    main()