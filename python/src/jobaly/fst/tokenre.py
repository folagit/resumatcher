# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 00:52:49 2014

@author: dlmu__000
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Aug 02 22:39:36 2014

@author: dlmu__000
"""

from restates import *        
    
class TokenRegex:
    
    def __init__(self, item):
        self.nextId = 1
        self.count = 0
        self.stateList = []
        self.createFst(item)
       
     
    def createState(self):
        sat = BaseState(self.nextId)
        self.stateList.append(sat)
        self.nextId += 1
        return sat
        
    def createMatchState(self, matcher):
        sat = MatchState(self.nextId, matcher )
        self.stateList.append(sat)
        self.nextId += 1
        return sat
        
    def createFst(self, item):
        start, end = self.compileItem(item)
        
        
        self.start = self.createState()  
        self.start.setStart() 
        for stat in  start:                  
            self.start.addNextState(stat)
         
        for stat in end:
            stat.setFinal()
       
    def compileItem(self, item):
         if type(item) is str:
                state = self.createMatchState(item)
                return [state], [state]
                
         elif type(item) is list:
             return self.compileArray(item)
             
         elif isinstance(item, Alternate) :
             return self.compileAlternate(item)
             
         elif isinstance(item, QuestionRepetition) :
             return self.compileQuestion(item)
             
         elif isinstance(item, PlusRepetition) :
             return self.compilePlus(item)   
             
         elif isinstance(item, StarRepetition) :
             return self.compileStar(item)
     
    def compileQuestion(self, item):  
        start = self.createState()               
        subStart, subEnd = self.compileItem(item.item)        
        
        start.extendNextStates(subStart)  
        subEnd.append(start)
        return [start], subEnd 
        
    def compileStar(self, item):
        start = self.createState()       
        subStart, subEnd = self.compileItem(item.item)
        end = self.createState()
        start.extendNextStates(subStart)
        start.extendNextStates(end)
        subEnd.extendNextStates(subStart)
        subEnd.extendNextStates(end)
        return [start], [end]
        
    def compilePlus(self, item):
        start = self.createState()        
        subStart, subEnd = self.compileItem(item.item)
        end = self.createState()
        start.extendNextStates(subStart)        
        subEnd.extendNextStates(subStart)
        subEnd.extendNextStates(end)
        return [start], [end]
             
    def compileAlternate(self, item):
        
        start = []
        end = []
        for subitem in item.alternates: 
            subStart, subEnd = self.compileItem(subitem)
            start.extend(subStart)
            end.extend(subEnd)
        return start, end
        
        
    def compileArray(self , array):
        
        startStates = None        
        current = None
        
        for item in array:
            subStart, subEnd = self.compileItem(item)
            if startStates is None:
                startStates = subStart
                current = subEnd
            else:           
                for stat in current:                   
                    stat.extendNextStates(subStart)                
                current = subEnd
                
        return startStates, current
               
        
    def match(self, seq ):
        self.current = self.startState
        i = 0  
        self.tempList = []
        result = self.greedyMatch(seq, i , self.current)
        
            
    def greedyMatch(   seq  , current ):
        i = 0             
        traq=[0]*len(seq)
        j = 0
        while i <  len(seq):
            item = seq[i]   
            while j < len(current.outArcs):
                arc = current.outArcs[j]
                if item == arc.inc :
                    self.tempList.append( (arc, item) )
                    traq[i] = j
                    current = arc.toState 
                    i += 1
                    j = 0
                    break
            if j == len(seq):
                i-=1
                j = traq[i] + 1
               
     
    
        