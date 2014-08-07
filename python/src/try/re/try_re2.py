# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 16:10:00 2014

@author: dlmu__000
"""
import re

def demo2():
    sent1 = 'nnnLDnn'
    sent2 = 'nnnLOLDnn'
    sent3 = 'nnnL,LOLDnn'
    sent4 = 'nnnL,LOLDnn'
    sent5 = 'nnnL,LDnn'
    
    match = re.search(r'L(OL)?D', sent1)
    match = re.search(r'L(,L)*(OL)?D', sent5)
    match = re.search(r'L((,L)*OL)|(OL)D', sent5)
    match = re.search(r'L(((,L)*OL)|(OL))D', sent4)
    match = re.search(r'L(((,L)*OL)|(OL))D', sent1)
    match = re.search(r'L(((,L)*OL)|(OL))?D', sent1)
    match = re.search(r'L(((,L)*OL)|(OL))?D', sent4)
    match = re.search(r'L(((,L)*OL)|(OL))?D', sent5)
    # If-statement after search() tests if it succeeded
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test3():
    sent1 = 'Dnnnn'     
    
    match = re.search(r'D', sent1)
    match = re.search(r'nn*', sent1)
    match = re.search(r'D|nn*', sent1)
    match = re.search(r'nn*|n', sent1)
    match = re.search(r'n|nn*', sent1)
    match = re.search(r'Dn|Dnn*', sent1)
    match = re.search(r'Dnn*|Dn', sent1)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test4():
    sent1 = 'Daaaa'     
    
    match = re.search(r'DD*', sent1)
    match = re.search(r'D*', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test5():
    sent1 = 'Daaba'     
    
  #  match = re.search(r'Da*b|Da*', sent1)
    match = re.search(r'Da*|Da*b', sent1)
   # match = re.search(r'D*', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test6():
    sent1 = 'Daababa'     
    
  #  match = re.search(r'Da*b|Da*', sent1)
    match = re.search(r'(ab)+', sent1)
    match = re.search(r'(ab|cd)+', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'        
        
def test7():
    sent1 = 'Dababcc'     

    match = re.search(r'(ab)+c*', sent1)
  #  match = re.search(r'(ab)+c+', sent1)
    match = re.search(r'D((ab)+|c*)', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
        
def test8():
    sent1 = 'Dababcc'     
   
    match = re.search(r'', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test9():
    sent1 = 'abbbccc'     
   
    match = re.search(r'a(bb|b*)', sent1)
    match = re.search(r'a(b*|bb)', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
   
def test10():
    sent1 = 'abbbccc'     
   
    match = re.search(r'.(bb|b*)', sent1)
    match = re.search(r'.(b*|bb|.*)', sent1)
    match = re.search(r'.(.*|bb)', sent1)
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test11():
    sent1 = 'fabbbccc'     
   
    match = re.search(r'.((ab)+)+', sent1)
   
    
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test12():
    sent1 = 'fabbbccc'        
    match = re.search(r'a|', sent1)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test13():
    sent1 = 'fabbbccc'        
    match = re.search(r'a*|f', sent1)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
def test14():
    sent1 = 'ab'        
    match = re.search(r'abc', sent1)
    match = re.search(r'abc|ab', sent1)
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
        
test14()