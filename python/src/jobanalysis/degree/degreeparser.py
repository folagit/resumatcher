# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 13:56:29 2014

@author: dlmu__000
"""
from degreelabeler import *

degreeMatcher1 = matcherCompiler.parse("DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)? DEGREE")

degreeMatchers = [ degreeMatcher1 ]


majorMatcher1 = matcherCompiler.parse("(IN| OF) DT? MAJOR " )
majorMatchers = [ majorMatcher1 ]

def getDegree(labeledArray):
    matcher = matchSent(degreeMatchers, labeledArray) 
    result = []    
    
    if matcher is not None:
        output = matcher.output()
        found = matcher.found 
        for item in output:
            if item[0] == 'DE_LEVEL':
                result.append(item[1])
    
    
    return result
    
def getMajor(labeledArray): 
    matcher = matchSent(majorMatchers, labeledArray) 
    result = []     
    if matcher is not None:
        output = matcher.output()
        found = matcher.found 
        for item in output:
            if item[0] == 'DE_LEVEL':
                result.append(item[1])
    
    return result
    
    
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
    