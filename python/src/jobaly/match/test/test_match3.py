# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 17:35:29 2014

@author: dlmu__000
"""

import sys
sys.path.append("..") 
import unittest
from matcher  import *
 

tokens1 = ["aaa","bbb","ccc","ddd"]
tokens2 = ["aaa","bbb","aaa","bbb","aaa","bbb","aaa","bbb","ccc","ddd"]

class TestMatch3(unittest.TestCase):   
    
    def test1(self):
        
         matcher1 = TokenMatcher("aaa") 
         matcher2 = TokenMatcher("bbb")   
         matcher3 = TokenMatcher("ccc") 
         
         seq1 = matcher1 + matcher2
         seq2 = matcher2 + matcher3
         
         self.assertEqual( seq1(tokens1), 2 )
         self.assertEqual( seq1.output(), ['aaa', 'bbb'] )
         
         self.assertEqual( seq2.findMatching(tokens1), 1 )
         self.assertEqual( seq2.output(), ['bbb', 'ccc'] )
         
    def test2(self):
        
         matcher1 = TokenMatcher("bbb") 
         matcher2 = TokenMatcher("aaa")   
         matcher3 = TokenMatcher("ccc") 
         
         seq1 = matcher1 | matcher2
         seq2 = matcher2 | matcher3
         
         self.assertEqual( seq1(tokens1), 1 )
         self.assertEqual( seq1.output(), ['aaa'] )
         
         self.assertEqual( seq2.findMatching(tokens1), 0 )
         self.assertEqual( seq2.output(), [ 'aaa'] )
         
    def test3(self):        
        matcher1 = TokenMatcher("aaa") 
        matcher2 = TokenMatcher(["bbb","ccc"]) 
        matcher3 = TokenMatcher([ "ddd"]) 
        
        alternate1 = AlternateMatcher([matcher1,matcher2])
        alternate2 = AlternateMatcher([matcher2,matcher3])
        alternate3 = AlternateMatcher([matcher3,matcher1])
        seq1 = alternate1 + alternate1
        
        self.assertEqual( alternate1(tokens1), 1 ) 
        self.assertEqual( alternate1.output(), [ 'aaa'] ) 
        self.assertEqual( alternate2(tokens1), -1 ) 
        self.assertEqual( alternate2.output(), None ) 
        self.assertEqual( alternate3(tokens1), 1 ) 
        self.assertEqual( alternate3.output(), [ 'aaa'] ) 
        self.assertEqual( seq1(tokens1), 3  ) 
        self.assertEqual( seq1.output(), [ 'aaa', 'bbb', 'ccc'] ) 

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMatch3)
    unittest.TextTestRunner(verbosity=2).run(suite)