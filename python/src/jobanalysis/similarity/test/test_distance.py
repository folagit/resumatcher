# -*- coding: utf-8 -*-
"""
Created on Thu Oct 02 23:36:17 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from jobaly.ontology.ontologylib import OntologyLib
import termdistance, pairdistance

sent1 = " HTML sdfdsf CSS rer erwer ewrw HTML  ".lower().split()
sent2 = " HTML dsf fd  sdfdsf CSS rer erwer ewrw HTML  ".lower().split()
sent3 = " HTML dsf fd  sdfdsf rer erwer ewrw HTML  ".lower().split()
sent4 = " CSS dsf fd  sdfdsf rer erwer ewrw HTML  ".lower().split()

sents = [sent1,sent2,sent3,sent4]
term1 = "HTML"
term2 = "CSS"

owlfile = "..\\..\\..\\jobaly\\ontology\\web_dev.owl"
ontology = OntologyLib(owlfile) 
ref1 = ontology.toURIRef("HTML")
ref2 = ontology.toURIRef("CSS")
terms1 = [ x.lower().split() for x in ontology.getTerms(ref1)]
terms2 = [ x.lower().split() for x in ontology.getTerms(ref2)]
print "terms1=" , terms1
print "terms2=" , terms2

def test1():
    dis1 = termdistance.getMinDistance( sent1, term1.lower(),  term2.lower() )
    print "dis1=", dis1
    
    dis2 = pairdistance.getMinDistance(sent1, terms1, terms2)
    print "dis2=", dis2
    
def test2():
    value1 = termdistance.getDistanceInSents( sents, term1.lower(),  term2.lower() )
    print "value1=" , value1
    
    value2 = pairdistance.getPairDistance(ontology, ref1, ref2, sents)
    print "value2=" , value2
    
    
def main(): 
    test2()
    
if __name__ == "__main__": 
    main()   