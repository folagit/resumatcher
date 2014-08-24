# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 12:07:50 2014

@author: dlmu__000
"""
import re

def test01():
    sent1 = 'ab+ab' 
    sent2 = 'ab\+ab'  
    match = re.search(r'\+ab', sent1)
    match = re.search(r'\\\+ab', sent2)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test02():
    sent1 = 'ab+ab' 
    sent2 = 'ab*\+\.ab'  
  #  match = re.search(r'\+ab', sent1)
    match = re.search(r'[(\\)(\+)(\*)(\.)]+', sent2)
    match = re.search(r'[\\\+\*\.]+', sent2)
    match = re.search(r'[(\\\+)(\\\.)]+', sent2)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test03():
    pattern = "r[a-zA-Z0-9_]+"
    sent1 = 'ab+ab' 
    sent2 = 'fefsdf2/34'  
  #  match = re.search(r'\+ab', sent1)
    match = re.search( r'[a-zA-Z0-9_/]+' , sent2)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
        
        
test02()