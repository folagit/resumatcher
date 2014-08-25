# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 21:32:29 2014

@author: dlmu__000
"""
import ply.lex as lex
import ply.yacc as yacc
import logging

import tokenlex

def testLex():
    #lexer = lex.lex(debug=1, module=tokenlex)
    lexer = lex.lex(module=tokenlex)
    data="dss dfdsf dfd 4=+"
    data=", : ; =-"
    data="(RT )"
    data="df+ df* (dfs)+ (er|df)?"
    data = "dd rr ee"
    lexer.input(data)
    
    print "---------------------------"
    print "data=", data
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

def test_parser():

    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger()
    lexer = lex.lex(module=tokenlex)
    parser = yacc.yacc(module=tokenlex,  debug=True)
    
    data=" ( ddddd )"
    data="ddddd 33"
    
    result = parser.parse(data, lexer=lexer)
    print "--- parse result----"
    print result

testLex()        
test_parser()