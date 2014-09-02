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
    ontology = OntologyLib("jobaly_v1.owl")
    ref = ontology.toURIRef("NOSQL")
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
     ontology = OntologyLib()    
     result = ontology.getLabels(ontology.ns.SoftwareDeveloper)
    
     result = ontology.getAllLabels()    
     #for entity, label  in result:
     #    print type(label), ":" , label
     
     termdict = ontology.getLabelDict()
     printLableDict( termdict )

def test_getTokenDict():
     ontology = OntologyLib()    
     printLableDict( ontology.tokenDict )
    
def main():
  # test_getTokenDict()
   #printGraph()
   # testFindSuperClass()
   testGetClassnames()

if __name__ == "__main__": 
    main()