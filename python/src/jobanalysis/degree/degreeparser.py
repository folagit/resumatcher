# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:56:29 2014

@author: dlmu__000
"""
from degreelabeler import *

degreeMatcher1 = matcherCompiler.parse("DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)? DEGREE")

degreeMatchers = [ degreeMacher1 ]


majorMatcher1 = matcherCompiler.parse("(IN| OF) DT? MAJOR " )
majorMatchers = [ majorMatcher1 ]

def getDegree(labeledArray):
    degreeSent, matcher = matchSent(degreeMatchers, sent) 
    result = []     
    if matcher is not None:
        output = matcher.output()
        found = matcher.found
    else:
        output = None
        found = None
        
    for item in ouput:
        if item[0] == 'DE_LEVEL':
            result.append(item[1])
    
    result
    
def getMajor(labeledArray): 
    degreeSent, matcher = matchSent(majorMatchers, sent) 
    result = []     
    if matcher is not None:
        output = matcher.output()
        found = matcher.found
    else:
        output = None
        found = None
        
    for item in ouput:
        if item[0] == 'DE_LEVEL':
            result.append(item[1])
    
    result
    
    
def parseDegreeSent( model, sent ): 
    degreeSent = JobSentence(sent.split())
    labeler.labelSentence(degreeSent)
 #   print degreeSent.printSentenct()  
#    f.write( degreeSent.printSentenct().get_string() +"\n\n" )
    labeledArray = degreeSent.getLabeledArray(labeler.ontoDict)
#    print degreeSent.printLabeledArray()    
    degrees =  getDegree(labeledArray)
    majors = getMajor(labeledArray)
    print degrees
    print majors
    model["degree"] = degrees
    model["major"] = majors
    