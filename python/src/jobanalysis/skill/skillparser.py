# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 17:04:12 2014

@author: dlmu__000
"""


import re
import os, sys
from nltk.tokenize import  word_tokenize

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from jobaly.ontology.ontologylib import OntologyLib
import os

class SkillParser():
    
    def __init__(self): 
        cd = os.path.dirname(__file__)
        print "cd=",cd
        owlfile = os.path.join(cd,"..\..\jobaly\ontology\web_dev.owl" )
        self.ontology = OntologyLib(owlfile)
        self.termDict = self.ontology.getFullDict()
        self.skillTerms = sorted( [ " "+x.lower()+" " for x in  self.termDict.keys() ] , key=len,  reverse=True) 
      #  print "self.skillTerms=",self.skillTerms
        
    def isSkillSent(self, sent):
        sent = sent.lower()
        for term in self.skillTerms:
            if sent.find(term) != -1:
         #       print sent.encode("GBK", "ignore")
                return True
        return False  
        
    def getSkillTermsList(self):
        terms = [ term.split() for term in self.skillTerms]
        
        return terms
        
    def parseSkill(self, jobModel, sent):
        skillset = []
        sent = " " +sent.lower()+ " "
        for term in self.skillTerms:
            if sent.find(term) != -1:
            #    print sent.encode("GBK", "ignore")   
                ontoClass =      self.termDict[term.strip()]  
                print "ontoClass=" , ontoClass
                skillset.append(ontoClass)
                sent = sent.replace(term, " " )
            #    print sent.encode("GBK", "ignore")
            #    print "---------"
                
        jobModel.addSkills( skillset )
        
def main(): 
   skillParser = SkillParser()
   
   terms = skillParser.skillTerms   
   
 #  terms = skillParser.getSkillTermsList()
   for term in terms:
       print term
    
if __name__ == "__main__": 
    main()        