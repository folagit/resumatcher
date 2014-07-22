# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 16:21:14 2014

@author: dlmu__000
"""

import nltk



def test_defaultTagger(tokens):
    
    default_tagger =  nltk.DefaultTagger('NN')
    print default_tagger.tag(tokens)
    
def test_chunk(sent):
    grammer = "9P: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammer)
    result = cp.parse(sent)
    print result
    
def test_wordpunct_tokenize(sent):
    from nltk.tokenize import wordpunct_tokenize
    print wordpunct_tokenize(sent)
    
def test_ne_chunk(sent):
    from nltk.chunk import ne_chunk
    print ne_chunk(sent)

def testConll2000():
    print ""

text = "And now for something completely different"
#test_wordpunct_tokenize(text)
text = "5+ years of experience in user interface development Expert knowledge in web technologies (JavaScript/CSS/HTML) Strong framework knowledge – JQuery (Must) and at least one of D3, Dojo, ExtJS, Angular, etc."
tokens = nltk.word_tokenize(text)
sent = nltk.pos_tag(tokens)
#print sent
test_ne_chunk(sent)
 
