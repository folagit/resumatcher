# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 17:15:55 2014

@author: dlmu__000
"""

from graphviz import Digraph

dot = Digraph(comment='The Round Table')
dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

# print(dot.source)
dot.render('round-table.gv', view=False)