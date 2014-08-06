# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 17:15:55 2014

@author: dlmu__000
"""

from graphviz import Digraph

def createPng(fileName):
    dotfile = 'C:\\graphviz-2.38\\release\\bin\\dot.exe'
    cmd=[dotfile, '-Tpng',  fileName+'.gv', "-o", fileName+".png"]
    #cmd=[dotfile, '-Tpdf', '-O', 'round-table.gv']
    returncode = subprocess.Popen(cmd).wait()
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
 
test1()