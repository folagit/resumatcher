# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 22:08:26 2014

@author: dlmu__000
"""

from graphviz import Digraph
import os
import subprocess
from fst import FstMachine, MatchState

def createPng(fileName):
    dotfile = 'C:\\graphviz-2.38\\release\\bin\\dot.exe'
    cmd=[dotfile, '-Tpng',  fileName+'.gv', "-o", fileName+".png"]
    #cmd=[dotfile, '-Tpdf', '-O', 'round-table.gv']
    returncode = subprocess.Popen(cmd).wait()
    os.startfile(os.path.normpath(fileName+".png"))
    print "returncode=", returncode
    
def createDotFile(dot,fileName):
    
    with open(fileName+".gv", "w") as f:
        f.write(dot.source)
    createPng(fileName)

class FstGraph:
    
    def __init__(self, fst):
        self.fst = fst
        self.graph = self.createDigraph()
        
    def createDigraph(self):
         dot = Digraph(comment='The Round Table', \
         node_attr={"shape":"circle"})
        
         dot.append("rankdir=LR;")
         dot.append('size="8,5"')
         
         return dot
    
    def parseFst(self):
        
        for state in  self.fst.stateList:
            
            if state.isStart :
                shape = "point"
              #  shape = "circle"
            elif state.isFinal:
                shape = "doublecircle"
            else :
                 shape = "circle"
            self.graph.node( state._id, state._id , {"shape":shape} )
        
        for state in  self.fst.stateList:
            for nextState in state.outStates:
                 if isinstance(nextState, MatchState):
                     label = nextState.matcher
                 else:
                     label = ""
                 self.graph.edge(state._id, nextState._id, label)
         
    def draw(self, fileName):
        self.parseFst()
        createDotFile(self.graph, fileName)
        