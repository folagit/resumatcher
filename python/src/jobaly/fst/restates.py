# -*- coding: utf-8 -*-
"""
Created on Wed Aug 06 01:13:29 2014

@author: dlmu__000
"""



class Alternate:
    
    def __init__(self, array):
        self.alternates = array 
        
class QuestionRepetition:
     def __init__(self, item):
        self.item = item 
        
class PlusRepetition:
     def __init__(self, item):
        self.item = item 
        
class StarRepetition:
     def __init__(self, item):
        self.item = item 

class BaseState:
    
     def __init__(self, _id):
         self._id = str(_id)
         self.outStates = []
         self.isFinal = False
         self.isStart = False
         
     def setFinal(self ):
         self.isFinal = True
         
     def setStart(self):
         self.isStart = True
     
     def addNextState(self, state):
         self.outStates.append(state)
         
     def extendNextStates(self, states):
         self.outStates.extend(states)
     
     def appendSelf(self, states):
         for stat in states:
             stat.addNextState(self)
    
class MatchState(BaseState):
    
    def __init__(self, _id, matcher):
        BaseState.__init__(self, _id )
        self.matcher = matcher
        
