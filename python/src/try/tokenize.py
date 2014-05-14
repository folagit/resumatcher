# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 08:28:49 2014

@author: dlmu__000
"""

import nltk

sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""
tokens = nltk.word_tokenize(sentence)

print tokens