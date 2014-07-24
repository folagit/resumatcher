# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 14:46:07 2014

@author: dlmu__000
"""
from textblob import TextBlob

def test1():
     b = TextBlob("And now for something completely different.")
    # print(b.parse())
     print b.parser
test1()