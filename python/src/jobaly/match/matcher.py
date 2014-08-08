# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 23:05:14 2014

@author: dlmu__000
"""
# such matcher how to handle repeat? 

class BaseMatcher:    
   
    def __init__(self):
        self.catch = []  
    
    def reset(self):
        self.catch = []    
        
    def match(self, tokens):
        return  -1
        
    def __call__(self, words):
        return self.match(words)
        
    def __or__(self, other):             
        
        return  AlternateMatcher([self,other]) 
        
    def __plus__(self, other):       
        return  SeqMatcher([self,other])
        
    def compileMatcher( args ):
         if type(args) is str:
             return TokenMatcher(args)
             
         if  type(args) is list:
           if all( type(x) is str for x  in args  ):
                return TokenMatcher(args)
           else:
               i = 0
               array = []
               newSeq = []
               while i < len(args):
                   if type(args[i]) is str:
                       array.append(args[i])
                   elif isinstance(args[i], BaseMatcher):
                       if len(array) > 0 :
                           newSeq.append(TokenMatcher(array))
                           array = []
                       newSeq.append.append(args[i])
                   else:
                       raise "unknow type matcher at"+str(i)
                   i+=1
               return newSeq                       
        
class TokenMatcher(BaseMatcher):
    
    def __init__(self, tokens):
        BaseMatcher.__init__(self)
        if type(tokens) is str:
            self.tokens = [tokens]
        elif type(tokens) is list:
            self.tokens = tokens
       
    def match(self, words):
        self.reset()
        if len(words) < len(self.tokens):
            return  -1
        
        i = 0 
        while i<len(self.tokens) and \
            self.tokens[i] == words[i]:
            self.catch.append(words[i])
            i += 1
        
        if i == len(self.tokens):
           return  i 
        else:
           return  -1

class CompMatcher(BaseMatcher): 
    
    def __init__(self, machers=None):
         BaseMatcher.__init__(self)
         if machers == None :
             self.machers = []
         elif type(machers) is list or \
             isinstance(machers, SeqMatcher ):
             self.machers = machers
         elif isinstance(machers, BaseMatcher ):
             self.machers = [machers]
    
    def append(self, macher):
        self.machers.append(macher)

    def extend(self, machers):
        self.machers.extend(machers)          
     
    def reset(self):
        BaseMatcher.reset(self)
        for catcher in self.machers:
            catcher.reset()
         
class SeqMatcher(CompMatcher):
    
    def __init__(self, machers=None):
         CompMatcher.__init__(self, machers)
    
    def match(self, words):
        self.reset()
       
        j = 0  # index of matcher 
        i = 0
        while j<len(self.machers) and ( i != -1):
            macher = self.machers[j]
            i =  macher(words)
            if i != -1:
               self.catch.extend(macher.catch) 
               words = words[i:]
               j +=1
               
        if j == len(self.machers):
            return  len(self.catch)
        else:
            return  -1
    
class AlternateMatcher(CompMatcher):
    
    def __init__(self, machers=None):
         CompMatcher.__init__(self, machers)
         
    def match(self, words):
        self.reset()
       
        j = 0  # index of matcher         
        while j<len(self.machers) :
            macher = self.machers[j]
            i =  macher(words)
            if i != -1:
               self.catch = macher.catch
               self.catchMacher = macher
               return i
            else:
               j+=1
               
        if j == len(self.machers):
            return  -1
            
    def reset(self):
        CompMatcher.reset(self)
        self.catchMacher = None 

# repreat matcher will not work very well like:
#    sent1 = 'abcabcabcabcde'        
#    match = re.search(r'(abc)*abcd', sent1)

class BaseRepeatMatcher(BaseMatcher):
    def __init__(self, matcher):
        BaseMatcher.__init__(self)
        self.matcher = matcher  
        
    def reset(self):
        BaseMatcher.reset(self)
        self.matcher.reset() 

class QuestionMatcher(BaseRepeatMatcher):
    
    def __init__(self, matcher):
        BaseRepeatMatcher.__init__(self, matcher)            
    
    def match(self, words): 
        self.reset()
        i = self.matcher(words)
        if i!=-1 :
            self.catch = self.matcher.catch
            return i
        else:
            return -1
            
class RepeatMatcher(BaseRepeatMatcher):
    
    def __init__(self, matcher, min=0, max=9999):
        BaseRepeatMatcher.__init__(self, matcher)   
        self.min = min
        self.max = max         
    
    def match(self, words): 
        self.reset()
        t = 0 
        while t < min :            
            i = self.matcher(words)
            if i!=-1 :
                self.catch.extend(self.matcher.catch)
                words = words[i:]
            else:
                break
        if t == min:
            return -1
        
        while t < max : 
            i = self.matcher(words)
            if i!=-1 :
                self.catch.extend(self.matcher.catch)
                words = words[i:]
            else:
                break
            
        return len(self.catch)
        
class StarMatcher(RepeatMatcher):
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher)
       
class PlusMatcher(RepeatMatcher):
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher, min=1) 
    
       
def findMatching( words, matcher):
    
    i = 0
    while i < len(words) :
        if matcher(words[i:]) != -1:
           return i
        else:
           i += 1
    return -1
    