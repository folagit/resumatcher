# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 17:41:12 2014

@author: dlmu__000
"""

import pygraphviz as pgv

G=pgv.AGraph()
G=pgv.AGraph(strict=False,directed=True)

G.add_node('a') # adds node 'a'
G.add_edge('b','c')

G.draw('test1.png')