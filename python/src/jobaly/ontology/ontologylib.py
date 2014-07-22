# -*- coding: utf-8 -*-
"""
Created on Thu Jul 03 16:28:22 2014

@author: dlmu__000
"""

import rdflib
from rdflib.namespace import RDF
from rdflib import URIRef, BNode, Literal,  RDFS

class OntologyLib:
    
    def __init__(self, owlFilename="jobaly_v1.owl", fileFormat="turtle"):
        self.g = rdflib.Graph()
        self.g.parse(owlFilename, format=fileFormat)
        self.ns = rdflib.Namespace("http://jobaly.com/ontology/")
        self.labels = self.getLabelList()        
        self.tokenDict = self.getTokenDict()        
        
    def toURIRef(self, name):
        return self.ns[name]
        
    def getSuperClass(self, subclass ):
        result = self.g.objects(subclass, predicate=RDFS.subClassOf)
        return result
        
    def getSubClasses(self, superClass):
        return self.g.subjects(RDFS.subClassOf, superClass)
        
    def getLabels(self, ref):
        return self.g.objects(ref, predicate=RDFS.label)
        
    def getAllLabels(self):
        return self.g.subject_objects( predicate=RDFS.label)
    
    def getLabelDict(self):   
        termDict = {}
        result = self.getAllLabels()    
        for entity, label  in result:           
            termDict[str(label)] = entity
        return termDict
        
    def getLabelList(self):
        self.termDict = self.getLabelDict()
        labels = self.termDict.keys()
        return  labels
        
    def getTokenDict(self):
        tokenDict = {}
        for label in self.labels :
            tokens = label.split()
            for token in tokens:
                if token in tokenDict :
                    tokenDict[token].append( label)
                else :
                     tokenDict[token] = [label]
        return tokenDict
        
def listGraph(g):
    for stmt in g:
        print type(stmt[0]), stmt[0]
        print type(stmt[1]),stmt[1]
        print type(stmt[2]),stmt[2]
        print "-----------------------"
        
        
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
    ontology = OntologyLib()
    ref = ontology.toURIRef("NOSQL")
    result = ontology.findSuperClass(ref)
    
    for o  in result:
        print type(o), ":" , o
        a = ontology.findSuperClass(o)
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
   test_getTokenDict()
    

if __name__ == "__main__": 
    main()

 
