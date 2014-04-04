# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 16:13:33 2014

@author: dlmu__000
"""

from bs4 import BeautifulSoup

def parsePage(page_content):
    soup = BeautifulSoup(page_content)
  #  print "title = %s" %soup.title
    aquo = soup.find("div", id="bvjl")
  #  aquo = summary =  soup.select(".aquo")
 #   print "aquo= %s " %aquo
  #  print "aquo.a= %s " %aquo.a
    print "aquo.a.href= %s " %aquo.a['href']
    summary =  soup.select(".summary")
  #  print "summary = %s" %summary

def main():
    fileName = "..\..\data\job_1.html"
    with open(fileName) as html_file:
        content = html_file.read()
   #     print content
        parsePage(content)
        
if __name__ == "__main__": 
    main()