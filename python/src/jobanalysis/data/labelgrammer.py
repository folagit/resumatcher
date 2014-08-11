# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 22:17:34 2014

@author: dlmu__000
"""

class LabelGrammer():
    
    def __init__(self, labelDict, ontoDict ):
        self.labelDict = self.lower(labelDict) 
        self.ontoDict = ontoDict
        self.ctreateLabelLists()  
        self.ctreateLabelTuples()
        
    def ctreateLabelTuples(self):
        self.labelTuples = []
        for label in self.labelDict.keys():  
            tokens = label.split()
            self.labelTuples.append( (tokens, self.labelDict[label]) )
        self.labelTuples = sorted (self.labelTuples, key = lambda x: len(x[0]), reverse=True)
    
    def ctreateLabelLists( self ):
        self.singleLabelList = []        
        self.multiLabelList =  [] 
        for label in self.labelDict.keys():  
            tokens = label.split()
            if len(tokens) == 1 :
                self.singleLabelList.append ( label ) 
            else :
                self.multiLabelList.append( [token.lower() for token in  tokens] )
        self.multiLabelList = sorted (self.multiLabelList, key=len, reverse=True)
    
    def labelSentence(self, sentence):
        for labelTuple in self.labelTuples:
            sentence.labelWithTuple(labelTuple)
    
    def lower(self, labelDict):
        newdict = {}
        for label in  labelDict.keys():
            tokens = label.split()
            if len(tokens) == 1 and len(tokens[0]) < 4 :
                newdict[label] = labelDict[label]
            else :
                newdict[label.lower()] = labelDict[label]
        return newdict