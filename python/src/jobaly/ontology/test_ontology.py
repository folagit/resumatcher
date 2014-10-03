# -*- coding: utf-8 -*-
"""
Created on Mon Sep 01 23:53:18 2014

@author: dlmu__000
"""
from ontologylib import OntologyLib
from rdflib import URIRef, BNode, Literal,  RDFS

def printGraph():
    ontology = OntologyLib("web_dev.owl")
    listGraph(ontology.g)

def listGraph(g):
    for stmt in g:
        print type(stmt[0]), stmt[0],"--n3--" , stmt[0].n3()
        print type(stmt[1]),stmt[1]
        print type(stmt[2]),stmt[2]
        print "-----------------------"
        
def testGetClassnames():
     ontology = OntologyLib("web_dev.owl")
     for n in ontology.getAllClassNames():
         print n
    
        
def findNode(g):
    
 #   print nosql
    result = g.objects(None, predicate=RDF.type)
    
    nosql = URIRef("http://jobaly.com/ontology/NOSQL")
    result = g.objects(nosql, predicate=RDFS.subClassOf)
    
    NS=rdflib.Namespace("http://jobaly.com/ontology/")
    result = g.objects(NS.NOSQL, predicate=RDFS.subClassOf)
    result = g.objects(NS.Embed, predicate=RDFS.subClassOf)
    result = g.objects(NS.Oracle, predicate=RDF.type)
    
    result = g.subjects(RDFS.subClassOf, NS.Role)
    result = g.subjects(RDF.type, NS.RDBS)
    
    result = g.label(NS.SoftwareDeveloper)
    result = g.preferredLabel(NS.SoftwareDeveloper)
    
    result = g.objects(NS.SoftwareDeveloper, predicate=RDFS.label)

    for o  in result:
        print o

def printLableDict(lableDict):
    
    for   label, entity in lableDict.iteritems():
        print label, ":", entity

def testFindSuperClass():
    ontology = OntologyLib("web_dev.owl")
    ref = ontology.toURIRef("Nosql_Database")
    print ref
    result = ontology.getSuperClass(ref)
    
    for o  in result:
        print type(o), ":" , o
        a = ontology.getSuperClass(o)
        for o2  in a:
            print type(o2), ":" , o2
            
def testGetSubClasses():
    ontology = OntologyLib()
    ref = ontology.toURIRef("NOSQL")
    result = ontology.getSubClasses(ref)
    
    for o  in result:
        print type(o), ":" , o
        
def testGetLabels():
     ontology = OntologyLib("web_dev.owl")    
     result = ontology.getLabels(ontology.ns.Nosql_Database)
     for r in result :
         print r
     return
     
     result = ontology.getAllLabels()    
     #for entity, label  in result:
     #    print type(label), ":" , label
     
     termdict = ontology.getLabelDict()
     printLableDict( termdict )

def test_getTokenDict():
     ontology = OntologyLib()    
     printLableDict( ontology.tokenDict )
     
def test_getLabelDict():
    ontology = OntologyLib("web_dev.owl")
    for  label , className in ontology.getLabelDict().items():           
          print  label ,"->" , className 
           
def test_getFullDict():
    ontology = OntologyLib("web_dev.owl")
    fullDict = ontology.getFullDict()
    for  label, className  in fullDict.items():           
           print  label ,"->" , className    
           
def test_getClasses():
    ontology = OntologyLib("web_dev.owl")
    classes = ontology.getClasses()
    for c in classes:
        print c
        
def test_isSuperClass():
    ontology = OntologyLib("web_dev.owl")
    ref1 = ontology.toURIRef("Nosql_Database")
    ref2 = ontology.toURIRef("Database")
    ref3 = ontology.toURIRef("Software")
    print ontology.isSuperClass( ref1, ref2 )
    print ontology.isSuperClass( ref1, ref3 )
    print ontology.isSuperClass( ref2, ref3 )
    print ontology.isSuperClass( ref3, ref2 )
    
def test_haveSameSuperClass():
    ontology = OntologyLib("web_dev.owl")
    ref1 = ontology.toURIRef("Database")
    ref2 = ontology.toURIRef("MySQL")
    ref3 = ontology.toURIRef("Software") 
    ref4 = ontology.toURIRef("Sql_Server")
    ref5 = ontology.toURIRef("Nosql_Database") 
    ref6 = ontology.toURIRef("Relational_Database") 
  #  print ref4
  #  result = ontology.getSuperClass(ref4)
    
    print ontology.haveSameSuperClass(ref4, ref2)
    print ontology.haveSameSuperClass(ref2, ref3)
    print ontology.haveSameSuperClass(ref5, ref6)
    print ontology.haveSameSuperClass(ref5, ref4)
    
def test_getSimilarityPair():
    ontology = OntologyLib("web_dev.owl")
    pairs = ontology.getSimilarityPairs()
    i = 0
    for pair in pairs:
        ref1, ref2 = pair   
        i+=1
        print i, " : " , (ref1.rsplit('#')[-1]) , "---" ,  (ref2.rsplit('#')[-1]) 
        
def test_getTerms():
    ontology = OntologyLib("web_dev.owl")
    ref1 = ontology.toURIRef("Nosql_Database")
    print ontology.getTerms(ref1)
    
def main():
  # test_getTokenDict()
   #printGraph()
   # testFindSuperClass()
  # test_getAllLabels()
  # testGetClassnames()
   # test_getClasses()
  #  test_getLabelDict()
  #   test_isSuperClass()
  #   testFindSuperClass()
   
  #   test_haveSameSuperClass()
   test_getSimilarityPair()
 #  test_getTerms()

if __name__ == "__main__": 
    main()