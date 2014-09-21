# -*- coding: utf-8 -*-
"""
Created on Sun Sep 07 14:30:39 2014

@author: dlmu__000
"""

from subprocess import Popen, PIPE
#from docx import opendocx, getdocumenttext
 
#http://stackoverflow.com/questions/5725278/python-help-using-pdfminer-as-a-library
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
 
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
   # codec = 'utf-8'
    codec = 'ascii'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str
 
def document_to_text(filename, file_path):
    if filename[-4:] == ".doc":
        cmd = ['antiword', file_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')
    elif filename[-5:] == ".docx":
        document = opendocx(file_path)
        paratextlist = getdocumenttext(document)
        newparatextlist = []
        for paratext in paratextlist:
            newparatextlist.append(paratext.encode("utf-8"))
        return '\n\n'.join(newparatextlist)
    elif filename[-4:] == ".odt":
        cmd = ['odt2txt', file_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')
    elif filename[-4:] == ".pdf":
        return convert_pdf_to_txt(file_path)
        
def getlines(txt):
    lines = txt.split("\n")
    i = 1
    print "line #", len(lines)
    for line in lines :
       print len(lines), ":",i, ":", len(line) , ">>" , line
       i+=1     
       if i > len(lines) -1  :
           break
        
def main(): 
  pdffile = "frank-cv.pdf"
#  pdffile = "simple1.pdf"
  pdffile = "Sandeep-Java.pdf"
  pdffile = "Huang-Liu.pdf"
  
  txt = convert_pdf_to_txt(pdffile)
  print "len of pdf =" , len(txt)
 # print txt[:100]
  getlines(txt)
    
if __name__ == "__main__": 
    main()   