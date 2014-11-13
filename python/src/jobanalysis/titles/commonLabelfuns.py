# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 13:34:37 2014

@author: dlmu__000
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from data.labeler import Labeler
from data.jobsentence import JobSentence
from jobaly.match.matcher  import *
from jobaly.match.matchercompiler  import MatcherCompiler

from  data import datautils


        
def labelSent(labeler, matcher, sent):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    i = matcher.findMatching(labeledArray) 
    return i, degreeSent   
         
class LabelMatcher(TokenMatcher): 
    
    def __init__(self, tokens):
        TokenMatcher.__init__(self, tokens, catchfun=lambda x:[ y[1] for y in x ] , outfun=lambda x: x )
        
    def getWord(self, item):
        return item[0]
        
class UnitLabelMatcher(UnitTokenMatcher): 
    
    def __init__(self, token):
        UnitTokenMatcher.__init__(self, token, catchfun=lambda x:[ y[1] for y in x ]  , outfun=lambda x: x )
        
    def getWord(self, item):
        return item[0]
        
       
        
class OriTextMatcher(TokenMatcher):     
    def __init__(self, tokens):
        TokenMatcher.__init__(self, tokens, catchfun=lambda x:[ y[2][0] for y in x ] , outfun=lambda x: x )
    
    # so one unit can only has one word     
    def getWord(self, item):
        return item[2][0]
        

def getOntoType(result , labeler):
 #   print "result=",result
    newresult = []
    for item in result:
     #   print " ^item=",item
        if item != [] and \
          labeler.ontoDict.has_key(item):
             newresult.append((labeler.ontoDict[item],item))
    return newresult

def labelSentByMatchers(matchers, sent):
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
#    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    matcher =  matchSent(matchers, labeledArray)
    return degreeSent, matcher

def matchSent(matchers, labeledArray):    
    for matcher in matchers:
        i = matcher.findMatching(labeledArray) 
        if i != -1:
            matcher.matchNum += 1
            return  matcher            
    return  None
    

    
def labelDegreeSet(matchers, data_set_name, outfileName,failfilename):
   
    for matcher in matchers:       
            matcher.matchNum = 0     
     
    data = datautils.loadJson(data_set_name)
   
    f = open(outfileName, "w")
    f2 = open(failfilename, "w")
    total = 0
    m = 0
    for item in data:
    #    print item
        sent = item[2]    
        sid = item[0]         
        matcher = None
        degreeSent, matcher = labelSentByMatchers(matchers, sent) 
     
        if matcher is not None:
            output = matcher.output()
            found = matcher.found
        else:
            output = None
            found = None
        
        print sid ,found, output 
        total += 1
        if matcher is not None :
            m+=1
            f.write( sent +"\n\n" )
            f.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
            f.write( str(found) + "   " + str(output) +"\n\n" )
        else :
            f2.write( sent +"\n\n" )
            f2.write( degreeSent.printLabeledArray().get_string() +"\n\n" )
             
    f2.write( "\n\n match="+ str( m) + "  total="+ str( total) + "  radio=" + str (float(m)/total) +"\n" )
             
    print "match=", m, "  total=", total, "  radio=", float(m)/total
    
    i = 0
    for matcher in matchers :
        i+=1
        print "matcher ", i, ":", matcher.matchNum
        f2.write( "\n matcher " + str( i) + ":" + str( matcher.matchNum ) )

matcherCompiler = MatcherCompiler(tokenMatcher=UnitLabelMatcher, defaultOutfun=getOntoType ,  debug=True) 