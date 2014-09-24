# -*- coding: utf-8 -*-
"""
Created on Wed Sep 24 14:24:03 2014

@author: dlmu__000
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from jobaly.pdf import pdftotxt

def fileToTxt(filepath):
     
    print "filepath =", filepath
    
    if filepath.endswith('.txt'):
        txtfile = filepath
    elif filepath.endswith('.pdf'):
        result = pdftotxt.pdftotxt(filepath)
        if result == 0 :
            txtfile = filepath[:-3]+"txt"
    
    print "txtfile =", filepath
    with open(txtfile, 'r') as content_file:
        content = content_file.read()
            
    return content
    
def main(): 
    filename = "Sandeep-Java.pdf"
    lines =  fileToTxt(filename)
    i = 0
    for line in lines:
        i+=1
        print i, ">" , line
    
if __name__ == "__main__": 
    main()
    