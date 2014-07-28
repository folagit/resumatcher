# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 22:17:34 2014

@author: dlmu__000
"""

class LabelGrammer():
    
    def __init__(self, labelDict ):
        self.labelDict = labelDict 
        self.ctreateLabelLists()
        
    
    def ctreateLabelLists( self ):
        self.singleLabelList = []        
        self.multiLabelList =  [] 
        for label in self.labelDict.keys():  
            tokens = label.split()
            if len(tokens) == 1 :
                self.singleLabelList.append ( label ) 
            else :
                self.multiLabelList.append(tokens)
        self.multiLabelList =sorted (self.multiLabelList, key=len, reverse=True)
    
    def labelSentence(self, sentence):
        pass