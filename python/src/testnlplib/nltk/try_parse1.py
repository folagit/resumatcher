# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 13:57:51 2014

@author: dlmu__000
"""

 	
from nltk import Nonterminal, nonterminals, Production

def test1():
    nt1 = Nonterminal('NP')
    nt2 = Nonterminal('VP')
     	
    print nt1.symbol()
     	
    S, NP, VP, PP = nonterminals('S, NP, VP, PP')
    N, V, P, DT = nonterminals('N, V, P, DT')
     	
    prod1 = Production(S, [NP, VP])
    prod2 = Production(NP, [DT, NP])
     	
    print prod1.lhs() 	
    print prod1.rhs() 	
    print prod1 == Production(S, [NP, VP]) 	
    print prod1 == prod2

import nltk

grammar = nltk.parse_cfg("""
    S -> NP VP
    PP -> P NP
    NP -> 'the' N | N PP | 'the' N PP
    VP -> V NP | V PP | V NP PP
    N -> 'cat'
    N -> 'dog'
    N -> 'rug'
    V -> 'chased'
    V -> 'sat'
    P -> 'in'
    P -> 'on'
    """) 

def test2():
    
    from nltk.parse import RecursiveDescentParser
    rd = RecursiveDescentParser(grammar)
    sentence1 = 'the cat chased the dog'.split()
    sentence2 = 'the cat chased the dog on the rug'.split()

 
    print rd.parse(sentence2)
     
def test3():
     nltk.parse.chart.demo(2,   trace=1, sent='I saw a dog', numparses=1)
 
def test4():
    grammar = nltk.data.load('grammars/large_grammars/atis.cfg')
  #  print grammar
    parser = nltk.parse.BottomUpChartParser(grammar)
    sentence2 = 'the cat chased the dog on the rug'.split()
    print parser.parse(sentence2)
    
def test5():
    fcp2 = nltk.parse.load_parser('grammars/book_grammars/feat0.fcfg')
    sentence2 = 'the cat chased the dog on the rug'.split()
    print fcp2.parse(sentence2)
    
test5()
