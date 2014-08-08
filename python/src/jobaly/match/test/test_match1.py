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

class TestMatch1(unittest.TestCase):    

    def test_token1(self):
        
        matcher = TokenMatcher("aaa") 
        self.assertEqual( matcher(tokens1), 1 )
        self.assertEqual( matcher.catch, ["aaa"] )
        
        matcher = TokenMatcher(["aaa", "bbb"]) 
        self.assertEqual( matcher(tokens1), 2 ) 
        self.assertEqual( matcher.catch, ["aaa", "bbb"] )
        
        matcher = TokenMatcher(["aaa", "ccc"]) 
        self.assertEqual( matcher(tokens1), -1 ) 
     
    def test_find(self):
         matcher = TokenMatcher(["aaa", "bbb"])
         self.assertEqual(findMatching(tokens1, matcher),0)
         
         matcher = TokenMatcher(["bbb", "ccc"])
         self.assertEqual(findMatching(tokens1, matcher),1)
         
         matcher = TokenMatcher(["ddd", "ccc"])
         self.assertEqual(findMatching(tokens1, matcher),-1)
         
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
         
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMatch1)
    unittest.TextTestRunner(verbosity=2).run(suite)

 