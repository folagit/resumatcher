# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 11:54:26 2014

@author: dlmu__000
 
"""

import re

def filterTagA():
    text = '''
    d sdsdfsd 
     fsd sdf  <a href="df" >inaaaa</a>ddf
     <p>dfesdf f</p>
     er fewvdf 
     '''
     
    notag = re.sub("<a.*?>|</a>", " ", text)
   
    print notag
    
def test_match():
    sent = "BS in Computer Science, Digital Media or similar technical degree with 3+ years of experience"
    
def demo1():
    import re
    line = "Cats are smarter than dogs"
    
    matchObj = re.match( r'(.*) are (.*?) .*', line, re.M|re.I)
    
    if matchObj:
       print "matchObj.group() : ", matchObj.group()
       print "matchObj.group(1) : ", matchObj.group(1)
       print "matchObj.group(2) : ", matchObj.group(2)
    else:
       print "No match!!"
 
def demo2():
    str = 'an example word:cat!!'
    match = re.search(r'word:\w\w\w', str)
    # If-statement after search() tests if it succeeded
    if match:                      
        print 'found', match.group() ## 'found word:cat'
    else:
        print 'did not find'
  
def demo3():
   sent = "dfsdf/sdfs dfds"
   match = re.search(r'\/', sent)
   
   if match:                      
        print 'found=', match.group() ## 'found word:cat'
   else:
        print 'did not find'
        
def testMatch():
   sent = "- ded dee"
   print re.match("\-",sent)  
   
testMatch()