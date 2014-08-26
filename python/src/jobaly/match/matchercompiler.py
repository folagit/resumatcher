# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 21:32:29 2014

@author: dlmu__000
"""

import ply.yacc as yacc
import matcheryacc
from matcher import UnitTokenMatcher

class MatcherCompiler:
    
    def __init__(self, tokenMatcher=UnitTokenMatcher, debug=False):
        matcheryacc.tokenMatcher = tokenMatcher
        self.parser = yacc.yacc(module=matcheryacc,  debug=debug) 
    
    def parse(self, s):
        return self.parser.parse(s)
       
