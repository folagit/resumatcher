# -*- coding: utf-8 -*-
"""
Created on Tue Aug 05 19:42:34 2014

@author: dlmu__000
"""
import subprocess

# dot -Tpdf -O round-table.gv

cmd=['dot', '-Tpdf', '-O', 'round-table.gv']
dotfile = 'C:\\graphviz-2.38\\release\\bin\\dot.exe'
cmd=[dotfile, '-Tpng',  '..\dot\\a.gv', "-o", "..\dot\\a.png"]
#cmd=[dotfile, '-Tpdf', '-O', 'round-table.gv']

returncode = subprocess.Popen(cmd).wait()