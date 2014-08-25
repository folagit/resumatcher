# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 21:32:29 2014

@author: dlmu__000
"""
import ply.lex as lex
import tokenlex

def testLex():
    #lexer = lex.lex(debug=1, module=tokenlex)
    lexer = lex.lex(module=tokenlex)
    data="dss dfdsf dfd 4=+"
    data=", : ; =-"
    data="(RT )"
    data="df+ df* (dfs)+ (er|df)?"
    lexer.input(data)
    
    print "---------------------------"
    print "data=", data
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok
        
testLex()