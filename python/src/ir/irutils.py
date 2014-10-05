# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 22:06:29 2014

@author: dlmu__000
"""

import re

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def clearReturn(txt):
     return re.sub("\\\n\-|\\\n", " ",txt)   
     
def processText(txt):
    txt = striphtml(txt)  
    txt = clearReturn(txt)
    return txt
    
 