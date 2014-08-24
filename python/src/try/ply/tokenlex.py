# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 11:36:11 2014

@author: dlmu__000
"""

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
t_TOKEN = r'[a-zA-Z0-9_/-]+'
t_OR = r'\|'


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
lexer = lex.lex()
lexer = lex.lex(debug=1)

# Test it out
data = '''
3 + 4 * 10
  + -20 *2
'''

data="ds-f/d+e (er4|df) a5+rr6 er3"

# Give the lexer some input
lexer.input(data)


print "---------------------------"
print "data=", data

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
    
    if __name__ == '__main__':
     lex.runmain()