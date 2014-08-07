# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 15:33:13 2014

@author: dlmu__000
"""

import unittest

class FixturesTest(unittest.TestCase):

    def setUp(self):
        print 'In setUp()'
        self.fixture = range(1, 10)

    def tearDown(self):
        print 'In tearDown()'
        del self.fixture

    def test(self):
        print 'in test()'
        self.failUnlessEqual(self.fixture, range(1, 10))
 
if __name__ == '__main__':
    unittest.main()