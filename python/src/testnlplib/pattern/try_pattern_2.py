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

def testTokenize():
    s = "I eat pizza with a fork."
  
    s = "B.S. in Computer Science, a related degree or its equivalent "     
    s = "What's this? This is a book."
 
    s = "Bachelor's degree in Computer Science or equivalent"
    s = "Bachelor’s degree in Computer Science or equivalent"   
   

    s = parse(s,
         tokenize = True,  # Tokenize the input, i.e. split punctuation from words.
             tags = False,  # Find part-of-speech tags.
           chunks = False,  # Find chunk tags, e.g. "the black cat" = NP = noun phrase.
        relations = False,  # Find relations between chunks.
          lemmata = False,  # Find word lemmata.
            light = False)

    print s.split() 
    
def test_findTonkens_1():
    s = "I eat pizza with a fork."
    s = "Bachelor's degree in Computer Science or equivalent"
    import pattern   
    result = pattern.text.find_tokens(s)
    print result
    
def test_findTonkens_2():
    s = "I eat pizza with a fork."
    s = "Bachelor's degree in Computer Science or equivalent"
    import pattern   
    parser = pattern.text.Parser()
    result = parser.find_tokens(s)
    result = pattern.text.en.tokenize(s)
    print result

def test_findTonkens_3():
    s = "I eat pizza with a fork."
    s = "Bachelor's degree in Computer Science or equivalent"
    s = "B.S. in Computer Science, a related degree or its equivalent "     
    s = "What's this? This is a book."  
    from pattern.en import tokenize     
    result = tokenize(s)
    print result
    
def test_parseTree():
    from pattern.en import parsetree
    sent = "What's this? This is a book."
    s = parsetree( sent , relations=True, lemmata=True)
    print repr(s)

testTokenize()