# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 11:36:11 2014

@author: dlmu__000
"""

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------

# List of token names.   This is always required
tokens = (
   'TOKEN',
   'PLUS',
   'QUES',
   'TIMES',
   'DOT',
   'OR',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_QUES   = r'\?'
t_TIMES   = r'\*'
t_DOT  = r'\.'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_OR = r'\|'
t_TOKEN = r'[a-zA-Z0-9_/-=:;,&$#@!\-<>%~]+'



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

# ---- rules ------

from jobaly.match.matcher  import *

def p_factorlist_factor(p):
    'factorlist : factor factor'
    elist = []
    elist.append(p[1])
    elist.append(p[2])
    p[0] = elist
    
def p_factorlist_factor1(p):
    'factorlist : factorlist factor'    
    p[0] = p[1].append(p[2])

def p_factor_token(p):
    'factor : TOKEN'
    p[0] = UnitTokenMatcher(p[1])
    
def p_factor_dot(p):
    'factor : DOT'
    p[0] = DotMatcher()

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print "error p", p

