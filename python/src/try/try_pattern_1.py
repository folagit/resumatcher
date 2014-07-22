# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 11:52:09 2014

@author: dlmu__000
"""
def test_parse():
    from pattern.en import parse
    from pattern.en import pprint 
    
    sent = 'I ate pizza.'
    sent = "Experience with mobile application development a plus: iPhone/iPad, Android, or Blackberry."
    sent = "3+ years web software development experience."
    pprint(parse(sent, relations=True, lemmata=True))

def test_wordnet():
    from pattern.en import wordnet
      
    word = "bird"
    word = "Java"
    word = "C++"
    word = "MongoDb"
    for s in wordnet.synsets(word) :
     
        print 'Definition:', s.gloss
        print '  Synonyms:', s.synonyms
        print ' Hypernyms:', s.hypernyms()
        print '  Hyponyms:', s.hyponyms()
        print '  Holonyms:', s.holonyms()
        print '  Meronyms:', s.meronyms()
  
  
def test_search():  
    from pattern.search import search
    from pattern.en import parsetree
      
    t = parsetree('big white rabbit')
    print t
    print
    print search('JJ', t) # all adjectives
    print search('NN', t) # all nouns
    print search('NP', t) # all noun phrases
    
def test_pattern():
    
   from pattern.search import Pattern
   from pattern.en import parsetree
  
   t = parsetree('Chuck Norris is cooler than Dolph.', lemmata=True)
   p = Pattern.fromstring('{NP} be * than {NP}')
   m = p.match(t)
   print m.group(1)
   print m.group(2)
   print t
 
    
test_pattern()