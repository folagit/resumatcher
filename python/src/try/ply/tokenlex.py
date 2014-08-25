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
