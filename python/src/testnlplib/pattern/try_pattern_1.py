# -*- coding: utf-8 -*-
"""
Created on Thu Jul 17 11:52:09 2014

@author: dlmu__000
"""
def test_parse():
    from pattern.en import parse, Text, Sentence
    from pattern.en import pprint 
    
   
    sent = "Experience with mobile application development a plus: iPhone/iPad, Android, or Blackberry."
    sent = "3+ years web software development experience."
    sent = "Bachelor's in Computer Science, Information Systems or a related study, is required."
    sent = 'I ate pizza.'
    sent = "Bachelor's in Computer Science is required."
    sent = "Bachelor 's Degree or 4 years equivalent professional experience ."
    sent = "A Master ’ s Degree or equivalent in Electrical Engineering , Computer Science , or other technical/engineering field with related programming experience and applicable work experience is required ."
    sent = "A Master's Degree or equivalent in Electrical Engineering , Computer Science , or other technical/engineering field with related programming experience and applicable work experience is required ."
    sent = "BS degree ( BSEE or BSCS strongly preferred , MSCS a plus ) and/or the equivalent in training and experience ."      
    
    result = parse(sent,
         tokenize = True,  # Tokenize the input, i.e. split punctuation from words.
             tags = True,  # Find part-of-speech tags.
           chunks = True,  # Find chunk tags, e.g. "the black cat" = NP = noun phrase.
        relations = True,  # Find relations between chunks.
          lemmata = True,  # Find word lemmata.
            light = True)
    pprint(result) 

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

    
def test_sentence():
    from pattern.en import parse, Text, Sentence
    from pattern.en import pprint 
    
    sent = "BS degree ( BSEE or BSCS strongly preferred , MSCS a plus ) and/or the equivalent in training and experience ."
    sent = "Bachelor's degree in Computer Science is required."  
    sent = "He created the robot and broke it after making it."
    result = parse(sent,
         tokenize = True,  # Tokenize the input, i.e. split punctuation from words.
             tags = True,  # Find part-of-speech tags.
           chunks = True,  # Find chunk tags, e.g. "the black cat" = NP = noun phrase.
        relations = True,  # Find relations between chunks.
          lemmata = True,  # Find word lemmata.
            light = True)
    pprint(result)
   
    sen = Sentence(result)
  #  print type(sen)
    print sen     

    for chunk in sen.chunks:
       print chunk.type, [(w.string, w.type) for w in chunk.words]
 
def test_findVerb():
    from pattern.en import parse, Text, Sentence
    from pattern.en import pprint 
    
   
    sent = "Bachelor's in Computer Science, Information Systems or a related study, is required."
    sent = 'I ate pizza.'
    sent = "Bachelor's in Computer Science is required."
    sent = "Bachelor 's Degree or 4 years equivalent professional experience ."
    sent = "A Master ’ s Degree or equivalent in Electrical Engineering , Computer Science , or other technical/engineering field with related programming experience and applicable work experience is required ."
    sent = "A Master's Degree or equivalent in Electrical Engineering , Computer Science , or other technical/engineering field with related programming experience and applicable work experience is required ."
    sent = "Bachelor ’ s degree in Computer Science or equivalent"
    sent = "Bachelor ' s degree in Computer Science or equivalent"
       
    
    result = parse(sent,
         tokenize = True,  # Tokenize the input, i.e. split punctuation from words.
             tags = True,  # Find part-of-speech tags.
            )
    pprint(result) 
    
  #  print type(result)
  #  print result         
    sen = Sentence(result)
  #  for word in sen:
 #       print word, word.type
    
    vlist = [ word.string for word in sen if word.type.startswith("V") ]
    print vlist
    
test_findVerb()