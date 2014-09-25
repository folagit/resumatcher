# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 23:29:40 2014

@author: dlmu__000
"""
import subprocess 
import re

def remove_non_ascii_2(text):
    return re.sub(r'[^\x00-\x7F]',' ', text)
    
def pdftotxt(filename):
    cmd = ["pdftotext.exe", "-nopgbrk", filename]    
    result = subprocess.call(cmd)
    return result

def pdftolines(filename):    
    cmd = ["pdftotext.exe", "-nopgbrk", filename]    
    result = subprocess.call(cmd)
    print filename , result 
    if result == 0 :
        prename = filename[0:-3]         
        txtname = prename+"txt"
        with open(txtname) as f:
            content = f.readlines()
            newcontent = []
            for line in content :
                newcontent.append(remove_non_ascii_2(line))
            return newcontent
            
def pdfToString(filename):    
    cmd = ["pdftotext.exe", "-nopgbrk", filename]    
    result = subprocess.call(cmd)
    print filename , result 
    if result == 0 :
        prename = filename[0:-3]         
        txtname = prename+"txt"
        with open(txtname) as f:
            content = f.read()            
            newcontent =remove_non_ascii_2(content)
            return newcontent
    
def main(): 
    filename = "files\\folder1\\Sandeep-Java.pdf"
    lines =  pdftolines(filename)
    i = 0
    for line in lines:
        i+=1
        print i, ">" , line
    
if __name__ == "__main__": 
    main()