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
   'LPAREN',
   'RPAREN',
)

literals = ['[',']','|','^']

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_QUES   = r'\?'
t_TIMES   = r'\*'
t_DOT  = r'\.'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
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
  
def p_expression_matcher(p):
    'expression : matcher'     
    p[0] =  p[1]  

def p_expression_matcherlist(p):
    'expression : matcherlist'     
    p[0] = SeqMatcher(p[1]) 
    
def p_expression_alt(p):
    'expression : altmatcher'     
    p[0] = p[1]    

def p_matcherlist_matcher(p):
    'matcherlist : matcherlist matcher'
    p[1].append(p[2])
    p[0] = p[1]  

def p_matcher_matcher(p):
    'matcherlist : matcher matcher'
 #   'matcherlist : matcher matcher'
    elist = []
    elist.append(p[1])
    elist.append(p[2])
    p[0] = elist    


def p_seq__par_matcherlist(p):
    'matcher : LPAREN matcherlist RPAREN'     
    p[0] = SeqMatcher(p[2])
    
def p_matcher_paren(p):
    'matcher : LPAREN matcher RPAREN'     
    p[0] = p[2]
    
    
def p_paren_alt(p):
    'matcher : LPAREN altmatcher RPAREN'     
    p[0] = p[2]

def p_alt_matcher(p):
    "altmatcher : altmatcher '|' matcher"   
    p[1].append(p[3])  
    p[0] =  p[1]  
    
def p_alt_matcher_matcher(p):
    "altmatcher : matcher '|' matcher"    
    p[0] = AlternateMatcher([p[1],p[3]])

def p_matcher_plus(p):
    'matcher : matcher PLUS'    
    p[0] = PlusMatcher(p[1])
    
def p_matcher_times(p):
    'matcher : matcher TIMES'    
    p[0] = StarMatcher(p[1])
    
def p_matcher_ques(p):
    'matcher : matcher QUES'    
    p[0] = QuestionMatcher(p[1])

def p_matcher_token(p):
    'matcher : TOKEN'
    p[0] = UnitTokenMatcher(p[1])
    
def p_matcher_dot(p):
    'matcher : DOT'
    p[0] = DotMatcher()

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    print "error p", p

