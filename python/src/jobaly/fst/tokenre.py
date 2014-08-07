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
from prettytable import PrettyTable

def printTrack(track):       
    x = PrettyTable(["state","last", "i", "j", "token"])   

    for  state, last , j, i  in   track:
           lastid = last._id if last is not None else ""
           matcher = state.matcher if isinstance(state,MatchState) else ""
           x.add_row([state._id, lastid, i, j,  matcher ])     
                    
           
    print x.get_string()   
    print
    
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
        start, end, couldpass = self.compileItem(item)        
        self.start = self.createState()  
        self.start.setStart() 
        for stat in  start:                  
            self.start.addNextState(stat)
         
        for stat in end:
            stat.setFinal()
        if couldpass:
            self.start.setFinal()
       
    def compileItem(self, item):
         if type(item) is str:
                state = self.createMatchState(item)
                return [state], [state], False
                
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
                     
        subStart, subEnd, couldpass = self.compileItem(item.item)         
        return subStart, subEnd, True 
        
    def compileStar(self, item):           
        subStart, subEnd, couldpass = self.compileItem(item.item)
        for stat in subEnd:
            stat.extendNextStates(subStart)
        return  subStart, subEnd, True 
        
    def compilePlus(self, item):             
        subStart, subEnd, couldpass = self.compileItem(item.item) 
        for stat in subEnd:
           stat.extendNextStates(subStart)        
        return subStart, subEnd, (False or couldpass)
             
    def compileAlternate(self, item):
        
        start = []
        end = []
        couldpass = False
        for subitem in item.alternates: 
            subStart, subEnd, subpass = self.compileItem(subitem)
            start.extend(subStart)
            end.extend(subEnd)
            couldpass = couldpass or subpass
        return start, end, couldpass
        
        
    def compileArray(self , array):        
        startStates = None        
        current = None
        couldpass = True
        for item in array:
            subStart, subEnd, subpass = self.compileItem(item)
            couldpass = couldpass and subpass            
            if startStates is None:
                startStates = subStart
                current = subEnd
            else:           
                for stat in current:                   
                    stat.extendNextStates(subStart) 
                if subpass:
                    subEnd.extend(current)
                current = subEnd
                
        return startStates, current, couldpass
        
    def _match(self, seq ):
        cur = self.start
        track = []    
        i = 0        
        j = 0      
        track.append((cur, None, -1, -1))    
        while i<len(seq) :
            token = seq[i]       
            if len(cur.outStates) == 0:                
                return track
            while j < len (cur.outStates):
                stat = cur.outStates[j]
                if token != stat.matcher :  
                    j+=1
                else:
                    track.append((stat, cur, j, i))
                    cur = stat
                    i += 1
                    j = 0
                    break
            if j == len (cur.outStates) :
                if cur.isFinal:                    
                    return track
                elif len(track) == 0:
                    i+=1
                    j = 0
                else:
                    stat , cur , j , i  = track.pop()
                    j += 1
            
       #     print "i=",i        
       #     printTrack(track)
                    
        return track            
    
        