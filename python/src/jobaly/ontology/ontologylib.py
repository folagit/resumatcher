# -*- coding: utf-8 -*-
"""
Created on Thu Jul 03 16:28:22 2014

@author: dlmu__000
"""

import rdflib
from rdflib.namespace import RDF
from rdflib import URIRef, BNode, Literal,  RDFS
import re
import copy
import os

class OntologyLib:
    
    def __init__(self, owlFilename, fileFormat="turtle", ns="http://www.jobaly.com/ontology/web_dev#"):
        self.g = rdflib.Graph()
        self.g.parse(owlFilename, format=fileFormat)
        self.ns = rdflib.Namespace(ns)
        self.labels = self.getLabelList()        
        self.tokenDict = self.getTokenDict()        
        
    def toURIRef(self, name):
        return self.ns[name]
        
    def getSuperClass(self, subclass ):
        result = self.g.objects(subclass, predicate=RDFS.subClassOf)
        return result
        
    def isSuperClass(self, subclass, superclass ):
        result = self.g.objects(subclass, predicate=RDFS.subClassOf) 
        return ( superclass in result )
        
    def haveSameSuperClass(self, subclass1, subclass2 ):
        result1 = self.g.objects(subclass1, predicate=RDFS.subClassOf) 
        result2 = self.g.objects(subclass2, predicate=RDFS.subClassOf) 
    
        for c in result1:
       #     print c 
            if c in result2: 
                return True
        return False
       
        
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
            className = entity.rsplit('#')[-1] 
            termDict[str(label)] = className           
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
        
    def getTerms(self, ref):
        terms = []
        term1 = (ref.rsplit('#')[-1]).replace("_", " " ) 
        terms.append(term1)
        result = self.g.objects(ref, predicate=RDFS.label)
        for c in result :
              c = str(c)
              if not (c in terms):
                  terms.append(c)
        return terms
        
    def getClassNameDict(self):       
       self.ClassNameDict={}
       classNode = URIRef("http://www.w3.org/2002/07/owl#Class")
       for s,p,o in self.g.triples( (None,  RDF.type, classNode) ):
           classname = s.rsplit('#')[-1]           
           self.ClassNameDict[ classname.replace("_", " ") ] = classname
       return self.ClassNameDict
       
    def getFullDict(self): 
        self.fullDict = {}
        for key, value in self.getLabelDict().items():
            self.fullDict[key.lower()] = value
        for key, value in self.getClassNameDict().items():
            self.fullDict[key.lower()] = value
        
        return self.fullDict
        
    def getClasses(self):
       classes = []
       classNode = URIRef("http://www.w3.org/2002/07/owl#Class")
       for s,p,o in self.g.triples( (None,  RDF.type, classNode) ):
           classes.append(s)
       return classes   
       
    def getSimilarityPairs(self):
        classes = self.getClasses()
        pairs = []
        for i in range(len(classes)):
            c1 = classes[i]
       #     print "c1=",c1
            for j in range(i+1,len(classes) ) :
                c2 = classes[j]
         #       print "c2 =",  c2                
         #       if self.isSuperClass(c1, c2) or self.isSuperClass(c2,c1) \
         #          or self.haveSameSuperClass(c1, c2) :
                if self.haveSameSuperClass(c1, c2):         #         
         #              print c1, c2
                       pairs.append( (c1, c2) )
        return pairs
                
def createOntology():
    path = os.path.dirname(os.path.realpath(__file__))
    owlfile = path+"\\"+"web_dev.owl"
    ontology = OntologyLib(owlfile)
 #   print "path=", path
    return ontology
