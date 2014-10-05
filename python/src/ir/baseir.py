# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 22:44:19 2014

@author: dlmu__000
"""

class BaseIr():
    
    def matchResume(self, resume):
        self.calculateScores(resume)
        self.jobs.sort(key=lambda x: x["score"], reverse=True)
        return self.jobs  