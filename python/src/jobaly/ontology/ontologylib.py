# -*- coding: utf-8 -*-
"""
Created on Thu Jul 03 16:28:22 2014

@author: dlmu__000
"""

import rdflib
from rdflib.namespace import RDF
from rdflib import URIRef, BNode, Literal,  RDFS

class OntologyLib:
    
    def __init__(self, owlFilename, fileFormat="turtle"):
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
        
    def getAllClassNames(self):       
       names=[]
       classNode = URIRef("http://www.w3.org/2002/07/owl#Class")
       for s,p,o in self.g.triples( (None,  RDF.type, classNode) ):
           names.append( s.rsplit('#')[-1] )
       return names
 
