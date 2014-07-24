# -*- coding: utf-8 -*-
"""
Created on Sun Jul 13 20:00:35 2014

@author: dlmu__000
"""

from textblob import TextBlob

text = '''
The titular threat of The Blob has always struck me as the ultimate movie
monster: an insatiably hungry, amoeba-like mass able to penetrate
virtually any safeguard, capable of--as a doomed doctor chillingly
describes it--"assimilating flesh on contact.
Snide comparisons to gelatin be damned, it's a concept with the most
devastating of potential consequences, not unlike the grey goo scenario
proposed by technological theorists fearful of
artificial intelligence run rampant.
'''

text = '''
Our client is looking for a Lead Web Developer 
to join their team for a permanent position.  
This person will Lead and Manage their Web Department.  
Manage servers, employees and projects.  Interact with 
clients and represent department in a professional way. 
'''

blob = TextBlob(text)
blob.tags           # [(u'The', u'DT'), (u'titular', u'JJ'),
                    #  (u'threat', u'NN'), (u'of', u'IN'), ...]

blob.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])
i = 1
for sentence in blob.sentences:

  #  print(sentence.sentiment.polarity)
    print i, ":", type(sentence) ,sentence
    i+=1
 
for sentence in blob.raw_sentences:

  #  print(sentence.sentiment.polarity)
    print i, ":", type(sentence) ,sentence
    i+=1   
