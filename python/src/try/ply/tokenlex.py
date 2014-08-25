# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 11:36:11 2014

@author: dlmu__000
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from jobaly.match.matcher  import *
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

def p_seq_termlist(p):
    'expression : termlist'     
    p[0] = SeqMatcher(p[1]) 
    
def p_expression_term(p):
    'expression : term'     
    p[0] = p[1] 

def p_termlist_term(p):
    'termlist : termlist term'
    p[1].append(p[2])
    p[0] = p[1]  

def p_term_term(p):
    'termlist : term term'
 #   'termlist : factor factor'
    elist = []
    elist.append(p[1])
    elist.append(p[2])
    p[0] = elist    


def p_term_termlist(p):
    'term : LPAREN termlist RPAREN'     
    p[0] = SeqMatcher(p[2])

def p_term_plus(p):
    'term : term PLUS'    
    p[0] = PlusMatcher(p[1])
    
def p_term_times(p):
    'term : term TIMES'    
    p[0] = StarMatcher(p[1])
    
def p_term_ques(p):
    'term : term QUES'    
    p[0] = QuestionMatcher(p[1])
    
def p_term_factor(p):
    'term : factor'    
    p[0] = p[1]

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

