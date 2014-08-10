# -*- coding: utf-8 -*-
"""
Created on Fri Aug 08 00:18:47 2014

@author: dlmu__000
"""


import sys
sys.path.append("..") 
import unittest
from matcher  import *
 

tokens1 = ["aaa","bbb","ccc","ddd"]
tokens2 = ["aaa","bbb","aaa","bbb","aaa","bbb","aaa","bbb","ccc","ddd"]

class TestMatch1(unittest.TestCase):    

    def test_token1(self):
        
        matcher = TokenMatcher("aaa") 
        self.assertEqual( matcher(tokens1), 1 )
        self.assertEqual( matcher.catch, ["aaa"] )
        self.assertEqual( matcher.output(), None )
        
        matcher = TokenMatcher(["aaa", "bbb"]) 
        self.assertEqual( matcher(tokens1), 2 ) 
        self.assertEqual( matcher.catch, ["aaa", "bbb"] )
        self.assertEqual( matcher.output(), None )
        
        matcher = TokenMatcher(["aaa", "ccc"]) 
        self.assertEqual( matcher(tokens1), -1 ) 
       
     
    def test_find(self):
         matcher = TokenMatcher(["aaa", "bbb"])
         self.assertEqual(matcher.findMatching(tokens1),0)
         self.assertEqual( matcher.output(), None )
         
         matcher = TokenMatcher(["bbb", "ccc"])
         self.assertEqual(matcher.findMatching(tokens1),1)
         self.assertEqual( matcher.output(), None )
         
         matcher = TokenMatcher(["ddd", "ccc"])
         self.assertEqual(matcher.findMatching(tokens1),-1)
         
    def test_seq1(self):  
        
        matcher1 = TokenMatcher("aaa") 
        matcher2 = TokenMatcher(["bbb","ccc"]) 
        matcher3 = TokenMatcher([ "ddd"]) 
        
        seq1 = SeqMatcher([matcher1,matcher2])
        seq2 = SeqMatcher([matcher1,matcher2,matcher3])
        seq3 = SeqMatcher([matcher1,matcher3])  
        
        self.assertEqual( seq1(tokens1), 3 )
        self.assertEqual( seq2(tokens1), 4 )
        self.assertEqual( seq3(tokens1), -1 )
        
    
    def test_Alternate(self):        
        matcher1 = TokenMatcher("aaa") 
        matcher2 = TokenMatcher(["bbb","ccc"]) 
        matcher3 = TokenMatcher([ "ddd"]) 
        
        alternate1 = AlternateMatcher([matcher1,matcher2])
        alternate2 = AlternateMatcher([matcher2,matcher3])
        alternate3 = AlternateMatcher([matcher1,matcher3])  
        
        self.assertEqual( alternate1(tokens1), 1 ) 
        self.assertEqual( alternate2(tokens1), -1 ) 
        
    def test_repeat(self):        
        matcher1 = StarMatcher(TokenMatcher(["aaa","bbb" ])) 
        matcher2 = StarMatcher(["bbb","ccc"]) 
        matcher3 = TokenMatcher("ccc") 
        
        seq1 = SeqMatcher([matcher1,matcher3])        
        
        self.assertEqual( matcher1(tokens2), 8 ) 
        self.assertEqual( seq1(tokens2), 9 ) 
        
    def test_output(self):
       
       class OutTokenMatcher(TokenMatcher):
           def __init__(self, tokens, catchfun=lambda x:x , outfun=lambda x: x):              
               TokenMatcher.__init__(self, tokens, catchfun, outfun)
               
       matcher1 = OutTokenMatcher("aaa")
       self.assertEqual(matcher1.findMatching(tokens1),0)
       self.assertEqual( matcher1.output(), ["aaa"] )
     
       matcher2 = OutTokenMatcher(["bbb", "ccc"])
       self.assertEqual(matcher2.findMatching(tokens1),1)
       self.assertEqual( matcher2.output(), ["bbb", "ccc"] )
     
       seq1 = SeqMatcher([matcher1,matcher2])      
       self.assertEqual(seq1(tokens1),3)        
       self.assertEqual( seq1.output(), ["aaa", "bbb", "ccc"] )
       
       alt1 = AlternateMatcher([matcher1,matcher2])      
       self.assertEqual(alt1.findMatching(tokens1),0)        
       self.assertEqual( alt1.output(), ["aaa"] )
       
       star1 = StarMatcher(OutTokenMatcher(["aaa","bbb" ])) 
       self.assertEqual(star1(tokens2),8)    
       self.assertEqual( star1.output(), ['aaa', 'bbb', 'aaa', 'bbb', 'aaa', 'bbb', 'aaa', 'bbb'] )
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMatch1)
    unittest.TextTestRunner(verbosity=2).run(suite)

 