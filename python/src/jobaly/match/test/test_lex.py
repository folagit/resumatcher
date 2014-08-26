# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 21:32:29 2014

@author: dlmu__000
"""
import ply.lex as lex
import ply.yacc as yacc
import logging

import sys
sys.path.append("..") 
import matcheryacc

def testLex(data):
    #lexer = lex.lex(debug=1, module=tokenlex)
    lexer = lex.lex(module=matcheryacc)   
    lexer.input(data)
    
    print "------- token result --------------------"
    print "data=", data
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

data=[]
data.append(".")
data.append("ddd")
data.append("(bbb*)")
data.append("ddddd 33")
data.append("ddddd 33 ccc")
data.append("ddddd 33 tt uuu")
data.append("ddddd ( 33 tt ) uuu")
data.append("ddd+")
data.append("bbb?")
data.append("bbb*")
data.append("bbb*+?")
data.append("aaa (dd bbb)* (dd? ,cc)+")

data.append("aaa | bbb")
data.append("aaa | bbb | ccc")
data.append("ddd (aaa | bbb) ")
data.append("( aaa | bbb | ccc ) ddd")
data.append("( aaa | bbb | ccc )* ddd")

 
testLex(data[4])

