# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 11:20:12 2014

@author: dlmu__000
"""
def testBasic():
    from pattern.en import referenced
    print referenced('hour')
    
    from pattern.en import conjugate, lemma, lexeme
    print lexeme('purr')
    print lemma('purring')
    print conjugate('purred', '3sg') # he / she / it

def testParse():
    
    from pattern.en import parse
    result = parse('I eat pizza with a fork.')
    result = parse('I eat pizza with a fork. I ate pizza.', tokenize=True )
        
    
    for s in result.split():
        print s
    return
    
    print type(result)
    print isinstance(result, unicode)
    print isinstance(result, basestring)
    print result.tags
    
def testParse2():
    
    from pattern.en import parse
    result = parse('I eat pizza with a fork.')
    result = parse('I eat pizza with a fork. I ate pizza.', tokenize=True, split=True  )
   
    for s in result :
        print s
        print "-----------"
    return
    
def testParse3():
    
    from pattern.en import parse
    result = parse('I eat pizza with a fork.')
    result = parse('The new Control Center design might not be final, or it might even go back to the old design. ', tokenize=True, chunks=True, split=True  )
   
    for s in result :
        print s
        print "-----------"
    return

def test_pprint():
    from pattern.en import parse
    from pattern.en import pprint 
    
    result = parse('I ate pizza.', relations=True, lemmata=True)
    pprint(result)    
    
def test_tag():
    from pattern.en import tag    
    s = "I eat pizza with a fork. You ate pizza."
    s = mytag(s)
    print s
  
from pattern.en import parse  
def mytag(s, tokenize=True, encoding="utf-8", **kwargs):
    """ Returns a list of (token, tag)-tuples from the given string.
    """
    tags = []
    for sentence in parse(s, tokenize, True, False, False, False, encoding, **kwargs).split():
        print  sentence       
        for token in sentence:
            tags.append((token[0], token[1]))
    return tags

testParse3()