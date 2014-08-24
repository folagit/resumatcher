# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 16:25:32 2014

@author: dlmu__000
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from jobaly.match.matcher  import *

import ply.lex as lex
import ply.yacc as yacc

# List of token names.   This is always required
tokens = (
   'TOKEN'   ,
   'DOT',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens

t_TOKEN = r'[a-zA-Z0-9_/-]+'
t_DOT  = r'\.'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)   


def expresslist_expression(p):
    'expresslist : expression expression'
    elist = []
    elist.append(p[1])
    elist.append(p[2])
    p[0] = elist  

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]    

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_token(p):
    'factor : TOKEN'
    p[0] = UnitTokenMatcher(p[1])
    
def p_factor_dot(p):
    'factor : DOT'
    p[0] = DotMatcher()
    
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print "error p", p

# Build the parser


import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

lex.lex(debug=True,debuglog=log)
parser = yacc.yacc(debug=True,debuglog=log)

data=" ( ddddd )"

data="  ddddd dd"


result = parser.parse(data)
print result