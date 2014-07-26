# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 16:57:48 2014

@author: dlmu__000
"""

import json
import nltk

def loadFile(fileName):
    f = open(fileName, "r")  
    data = f.read()      
    sents = json.loads(data) 
    for sent in sents:
        sent[1] = nltk.word_tokenize(sent[1])
        print sent[1]
    return sents

def rule1(sents):
    ignoreList = [u'-', u',',u'.',u'or',u'and' ]
    pass
   
def testRule1():
    sent = "HTML5, CSS, JavaScript, Sencha ExtJS, JQuery Mobile, and REST."
    tokens = nltk.word_tokenize(sent)
    print tokens

def main():   
    testRule1() 
    
if __name__ == "__main__": 
    main()