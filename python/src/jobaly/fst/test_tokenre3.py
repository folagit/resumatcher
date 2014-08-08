# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 16:18:09 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 15:47:28 2014

@author: dlmu__000
"""

 
import unittest
from tokenre  import *
from drawfst import FstGraph

tokens1 = ["aaa","bbb","ccc","ddd"]

class TestTokenre3(unittest.TestCase):    

    def test_seq1(self):
        self.assertTrue(TokenRegex(["bbb","ccc"]).match(tokens1)) 
        self.assertFalse(TokenRegex(["bbb","ddd"]).match(tokens1)) 
         
    def test_Alternate(self):
        self.assertTrue(TokenRegex(Alternate(["bbb","ccc"])).match(tokens1)) 
        self.assertTrue(TokenRegex(["bbb",Alternate(["bbb","ccc"]),"ddd"]).match(tokens1)) 
        
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTokenre3)
    unittest.TextTestRunner(verbosity=2).run(suite)

 