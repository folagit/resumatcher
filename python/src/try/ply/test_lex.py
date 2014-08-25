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
    parser = yacc.yacc(module=tokenlex,  debug=True, debuglog=log) 
    
    result = parser.parse(data, lexer=lexer)
    print "\n\n--- parse result----"
    print result
    
    
def test_parser_with_array(datas):

    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger()
    lexer = lex.lex(module=tokenlex)
   # parser = yacc.yacc(module=tokenlex,  debug=1, debuglog=log) 
    parser = yacc.yacc(module=tokenlex,  debug=1) 
    
    print "\n\n--- parse result----"
    for data in datas :
        result = parser.parse(data, lexer=lexer)        
        print result

data=[]
data.append(".")
data.append("ddd")
data.append("(bbb*)")
data.append("ddddd 33")
data.append("ddddd 33 tt uuu")
data.append("ddd+")
data.append("bbb?")
data.append("bbb*")
data.append("bbb*+?")
data.append("[ddddd 33 tt uuu]")
 
#testLex(data[4])
#test_parser_with_array(data)
#test_parser(data[3])
test_parser_with_array(data)
