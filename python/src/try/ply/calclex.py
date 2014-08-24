# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 11:30:52 2014

@author: dlmu__000
"""

# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

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

# Build the lexer
#lexer = lex.lex()
lexer = lex.lex(debug=2)


# Test it out
data = '''
3 + 4 * 10
  + -20 *2
'''

data="5+6"

# Give the lexer some input
lexer.input(data)

print "---------------------------"
print "data=", data

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
    
