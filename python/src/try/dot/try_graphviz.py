# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 17:15:55 2014

@author: dlmu__000
"""

from graphviz import Digraph
import os

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

def test1():
    dot = Digraph(comment='The Round Table')
    dot.node('A', 'King Arthur')
    dot.node('B', 'Sir Bedevere the Wise')
    dot.node('L', 'Sir Lancelot the Brave')
    
    dot.edges(['AB', 'AL'])
    dot.edge('B', 'L', constraint='false')
    createDotFile(dot, "test1")
    # print(dot.source)

def test2():
    dot = Digraph(comment='The Round Table', \
        node_attr={"shape":"circle"})
        
    dot.append("rankdir=LR;")
    dot.append('size="8,5"')
        
    dot.node('A', "", {"shape":"doublecircle"} )
    dot.node('B' ,"" )
    dot.node('L', ""  )
    dot.node('S', "", {"shape":"point"} )
     
    dot.edge('S', 'A', "e")
    dot.edge('A', 'B', "a")
    dot.edge('B', 'L', "b")
    dot.edge('L', 'L', "l")
   # dot.edge('B', 'L', constraint='false')
    createDotFile(dot, "outfiles\\test2")

 
    
test2()