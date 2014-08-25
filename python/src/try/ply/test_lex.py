# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 21:32:29 2014

@author: dlmu__000
"""
import ply.lex as lex
import ply.yacc as yacc
import logging

import tokenlex



def testLex(data):
    #lexer = lex.lex(debug=1, module=tokenlex)
    lexer = lex.lex(module=tokenlex)   
    lexer.input(data)
    
    print "------- token result --------------------"
    print "data=", data
    
    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        print tok

def test_parser(data):

    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger()
    lexer = lex.lex(module=tokenlex)
    parser = yacc.yacc(module=tokenlex,  debug=True) 
    
    result = parser.parse(data, lexer=lexer)
    print "\n\n--- parse result----"
    print result

data1="ddd"
data2="ddddd 33"
data3="ddddd 33"

data = data3

testLex(data3)        
test_parser(data3)