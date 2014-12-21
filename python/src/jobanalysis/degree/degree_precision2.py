# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 21:06:41 2014

@author: dlmu__000
"""

from degreelabeler import matcherCompiler, labelDegreeSet

import random

dumpLam2 = lambda x: x[0] + " | " + str( x[1] ) + " | " + x[2]

pattern1 = matcherCompiler.parse("DE_LEVEL (DEGREE)? (IN|OF) MAJOR")
pattern2 = matcherCompiler.parse(" (MAJOR_DEGREE|DE_LEVEL) OR  DEGREE_JJ DEGREE") 
pattern3 = matcherCompiler.parse("DE_LEVEL (DEGREE)? PREFER_VBD")
pattern4 = matcherCompiler.parse("DE_LEVEL BE (PREFER_VBD|PREFER_JJ) ")
#pattern5 = matcherCompiler.parse("MAJOR_DEGREE")
pattern5 = matcherCompiler.parse("DE_LEVEL OR (HIGHER_JJ)? (DEGREE_JJ)? DEGREE")

pattern6 = matcherCompiler.parse("DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)?  DEGREE")

degree_matchers_local = [ pattern1, pattern2, pattern3, pattern4, pattern5, pattern6 ] 

def getRadom(srcname, n):      
      data = datautils.loadJson(srcname)
      randomData = []
      print "data len=", len(data)
      r = random.randrange(0, len(data) )
      print "r=", r
      
      for i in range(n):
          r = random.randrange(0, len(data) )
          line = data[r]
          randomData.append(line)
    #      print i, ">>" , line
      
      target_set_name = srcname + "_random"+str(n)
      datautils.dumpTwo(randomData, target_set_name , dumpLam2)    

def testDegree(srcname, n):
   target_set_name = srcname + "_random"+str(n)
   outfileName = target_set_name + "_array.txt"
   failfilename =  target_set_name + "_array_fail.txt"
  
   labelDegreeSet(degree_matchers_local, target_set_name,outfileName, failfilename) 
      
def main():    
   
    src_set_name = "output2\\degree_sents"  
    n = 500
  #  getRadom(src_set_name, n)
    testDegree(src_set_name, n)
  
if __name__ == "__main__": 
    main()