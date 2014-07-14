# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 11:54:26 2014

@author: dlmu__000
 
"""

import re

def filterTagA():
    text = '''
    d sdsdfsd 
     fsd sdf  <a href="df" >inaaaa</a>ddf
     <p>dfesdf f</p>
     er fewvdf 
     '''
     
    notag = re.sub("<a.*?>|</a>", " ", text)
   
    print notag
    
filterTagA()