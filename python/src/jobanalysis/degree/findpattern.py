# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 12:29:07 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from data.jobsentence import JobSentence
from jobaly.match.matcher  import *



from data.jobsentence import JobSentence
from degreelabeler import *
from degree_patterns import *
from major_patterns import *


    

def main(): 
      
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree1.txt"
   failfilename =  "output\\data3_degree1_fail.txt"

   matcher =  degreeSeq8  
 #  matcher =  degreeSeq3
  # matcher = matcher7
   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree1.txt"  
   failfilename =  "output\\data1_degree1_fail.txt"
   
   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree5.txt"  
   failfilename =  "output\\data1_degree5_fail.txt"
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree5.txt"
   failfilename =  "output\\data3_degree5_fail.txt"

   target_set_name = "output\\degree_1"   
   outfileName = "output\\data1_degree6.txt"  
   failfilename =  "output\\data1_degree6_fail.txt"
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree6.txt"
   failfilename =  "output\\data3_degree6_fail.txt"
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_degree_array.txt"
   failfilename =  "output\\data3_degree_array_fail.txt"
   
   matchers = [ degreeSeq2, degreeSeq4, degreeSeq6, degreeSeq7, degreeSeq8 ]   
   
   target_set_name = "output\\degree_3"
   outfileName = "output\\data3_major_array.txt"
   failfilename =  "output\\data3_major_array_fail.txt"   
   
   matchers = [majorSeq1, majorSeq2, majorSeq3,majorSeq4, majorSeq5]

   labelDegreeSet(matchers, target_set_name,outfileName, failfilename) 
   


if __name__ == "__main__": 
    main() 