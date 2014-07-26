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
    
    comb4 = lambda x : tokenFind("install")( x ) and tokenFind("als")( x )
    print "comb4" , comb4(words)
 
def test_TokenMatcher():
    sent = "You can also install Spyder from its zip source package" 
    words = sent.split()
   
    matcher1 = TokenMatcher("install")
    matcher2 = TokenMatcher("insta")
    print "matcher : " , matcher1(words)
    
    match_comb1 = matcher1 or  matcher2
    match_comb2 = matcher1 and  matcher2
    print "matcher 1 or 2 : " , match_comb1(words)
    print "matcher 1 and 2 : " , match_comb2(words)
    
def test_complex():
    sent = "You can also install Spyder from its zip source package" 
    words = sent.split()
    
    match_comb3 = ( TokenMatcher("install") | TokenMatcher("insta") ) & TokenMatcher("also") 
    print "matcher 3 : " , match_comb3(words)    
    
    match_comb4 =  TokenMatcher("inuustall") & TokenMatcher("insta") & TokenMatcher("also") 
    print "matcher 4 : " , match_comb4(words)  

    match_comb5 = ( TokenMatcher("inuustall") & TokenMatcher("insta") ) & TokenMatcher("also") 
    print "matcher 5 : " , match_comb5(words)      
    
    match_comb6 = ( TokenMatcher("inuustall") & TokenMatcher("insta")  )
    print type(match_comb6)
    print "matcher 6 : " , match_comb6(words)  
    
    match_comb7 = ~ TokenMatcher("inuustall") 
    print "matcher 7 : " , match_comb7(words) 
    
    match_comb8 = ( ~ TokenMatcher("inuustall") ) & TokenMatcher("install")
    print "matcher 8 : " , match_comb8(words) 
   
 
def test_complex2():   
    sent = "You can also install Spyder from its zip source package" 
    words = sent.split()
    
    match_comb4 =  TokenMatcher("install") & TokenMatcher("zip")
    match_comb5 = match_comb4 & TokenMatcher("also")
    match_comb6 = TokenMatcher("also") & match_comb4  
    print "matcher 4 : " , match_comb4(words)  
    print "matcher 5 : " , match_comb5(words)  
    print "matcher 6 : " , match_comb6(words) 
    
def main():   
  #  test_tokenMatch() 
    test_complex()
  #  test_comb()
    
if __name__ == "__main__": 
    main()