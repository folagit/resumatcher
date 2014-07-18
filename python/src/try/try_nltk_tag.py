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

text = "And now for something completely different"
tokens = nltk.word_tokenize(text)
sent = nltk.pos_tag(tokens)
print sent
 
test_chunk(sent)