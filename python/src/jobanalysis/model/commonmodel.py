# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 18:17:56 2014

@author: dlmu__000
"""

class CommonModel():
    
    def __init__(self):       
        self.majors = set()
        self.degees = set()
        self.skills = set()
        
    def addDegrees(self, degrees):
        for a in degrees:
            self.degees.add(a)            
            
    def addMajors(self, majors):
        for a in majors:
            self.majors.add(a)
            
    def addSkills(self, skills):
        for a in skills:
            self.skills.add(a)
            
    def serialize(self):
        objDict = {}
        objDict["degrees"] = list(self.degees)
        objDict["majors"] = list(self.majors)
        objDict["skills"] = list(self.skills)
        
        return objDict