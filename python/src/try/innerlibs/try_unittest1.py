# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 15:25:08 2014

@author: dlmu__000
"""

import unittest

class SimplisticTest(unittest.TestCase):

    def test(self):
        self.failUnless(False,"no good")
        
class OutcomesTest(unittest.TestCase):

    def testPass(self):
        return

    def testFail(self):
        self.failIf(True)

    def testError(self):
        raise RuntimeError('Test error!')
        
class TruthTest(unittest.TestCase):

    def testFailUnless(self):
        self.failUnless(True)

    def testAssertTrue(self):
        self.assertTrue(True)
        
        self.assertTrue(False)

    def testFailIf(self):
        self.failIf(False)

    def testAssertFalse(self):
        self.assertFalse(False)
        
class EqualityTest(unittest.TestCase):

    def testEqual(self):
        self.failUnlessEqual(1, 3-2)

    def testNotEqual(self):
        self.failIfEqual(2, 3-2)


if __name__ == '__main__':
    unittest.main( )