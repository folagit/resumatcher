# -*- coding: utf-8 -*-
"""
Created on Sat Aug 02 22:39:36 2014

@author: dlmu__000
"""



class Alternate:
    
    def __init__(self, array):
        self.alternates = array
        
class StateFrag:
    
    def __init__(self, start, outList):
        self.startState = start
        self.outList = outList

class BaseState:
    
     def __init__(self, _id):
         self._id = _id
         self.outStates = []
         self.final = False
         self.start = False
         
     def setFinal(self ):
         self.final = True
         
     def setStart(self):
         self.start = True
     
     def addNextState(self, state):
         self.outStates.append(state)
    
    
class MatchState(BaseState):
    
    def __init__(self, _id, matcher):
        BaseState.__init__(self, _id )
        self.matcher = matcher
        
        
    
class FstMachine:
    
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
        self.start, self.end = self.compileItem(item)
        self.end.setFinal()
        
    def compileItem(self, item):
         if type(item) is str:
                state = self.createMatchState(item)
                return state, state
         if type(item) is Alternate:
             return self.compileAlternate(item)
         if type(item) is list:
             return self.compileArray(item)
             
    def compileAlternate(self, item):
        
        start = self.createState()
        end = self.createState()
        for subitem in item.alternates: 
            subStart, subEnd = self.compileItem(subitem)
            start.addNextState(subStart)
            subEnd.addNextState(end)
        return start, end
        
        
    def compileArray(self , array):
        
        startState = None        
        current = None
        
        for item in array:
            subStart, subEnd = self.compileItem(item)
            if startState is None:
                startState = subStart
                current = subEnd
            else:
                current.addNextState(subStart)
                current = subEnd
                
        return startState, current
               
        
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
               
     
    
        