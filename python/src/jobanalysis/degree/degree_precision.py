# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 16:45:03 2014

@author: dlmu__000
"""
from degreelabeler import *
from degree_patterns import *
import random

dumpLam2 = lambda x: x[0] + " | " + str( x[1] ) + " | " + x[2]


degree_matchers_local = [ degreeSeq2  ]
degree_matchers_local = [ degreeSeq2, degreeSeq4 ] 

degree_matchers_local = [ degreeSeq2, degreeSeq4, degreeSeq6, degreeSeq7, degreeSeq8,degreeSeq9 ] 

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
    src_set_name = "output\\degree_3"
    src_set_name = "output\\degree_after_0610"  
    n = 100
  #    getRadom(src_set_name, n)
    testDegree(src_set_name, n)
  
if __name__ == "__main__": 
    main()