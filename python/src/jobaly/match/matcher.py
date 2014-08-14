# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 23:05:14 2014

@author: dlmu__000
"""
# such matcher how to handle repeat? 

class BaseMatcher:    
   
    def __init__(self, catchfun=lambda x:x , outfun=lambda x: x):
        self.catch = []  
        self.catchfun = catchfun
        self.outfun = outfun
        self.found = None
        
    def setCatchFun(self, catchfun):
        self.catchfun = catchfun
        
    def setOutFun(self, outfun):
        self.outfun = outfun
    
    def reset(self):
        self.catch = []   
        self.found = None
        
    def match(self, tokens):
        return  -1
        
    def __call__(self, words):
        return self.match(words)
        
    def __or__(self, other):             
        if isinstance(self, AlternateMatcher ) :
            self.append(other)
            return self
        else: 
            return  AlternateMatcher([self,other]) 
        
    def __add__(self, other):      
        if isinstance(self, SeqMatcher ) :
            self.append(other)
            return self
        else: 
            return  SeqMatcher([self,other])
        
           
    def findMatching( self, words):        
        i = 0
        while i < len(words) :
            j = self.match(words[i:]) 
            if j != -1:
               self.found = (i,j)
               return i
            else:
               i += 1
        return -1
        
    def getFound(self, words):
        if self.found is not None:
            return words[self.found[0]:self.found[1]]
        else :
            return None
        
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
    
    def __init__(self, tokens, catchfun=lambda x:x , outfun=lambda x: x):        
        BaseMatcher.__init__(self, catchfun, outfun)
        if type(tokens) is str:
            self.tokens = [tokens]
        elif type(tokens) is list:
            self.tokens = tokens        
    
    @staticmethod    
    def getWord(item):
        return item
    
    @staticmethod    
    def defaultCatchfun(item):
        return item
    
    @staticmethod    
    def defaultOutfun(item):
        return None
    
    def output(self):  
        return self.outfun(self.catch)
       
    def match(self, words):
        self.reset()
        if len(words) < len(self.tokens):
            return  -1
        
        i = 0 
        while i<len(self.tokens) and \
            self.tokens[i] == self.getWord(words[i]):
            self.catch.append(self.catchfun(words[i]))
            i += 1
        
        if i == len(self.tokens):
           return  i 
        else:
           return  -1

class CompMatcher(BaseMatcher): 
    
    def __init__(self, machers=None , catchfun=lambda x:x , outfun=lambda x: None):
         BaseMatcher.__init__(self, catchfun,outfun )
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
    
    def __init__(self, machers=None, catchfun=lambda x:x , outfun=lambda x: x):
         CompMatcher.__init__(self, machers, catchfun, outfun )
    
    def match(self, words):
        self.reset()
        i = 0
        j = 0  # index of matcher        
        last = 0
        while j<len(self.machers) and ( i != -1):
            macher = self.machers[j]
            i =  macher(words)
            if i != -1:
                if not isinstance(macher, RepeatMatcher) or \
                    j==len(self.machers)-1 or i==0:
                   self.catch.extend(macher.catch) 
                   words = words[i:]
                   j +=1  
                   last += i
                else :                  
                   i = self.matchWithRepeat(macher, j,  words) 
                   if i != -1:
                       last += i
                       return last
               
        if j == len(self.machers):
            return  last
        else:
            return  -1
     
    def matchWithRepeat(self, matcher, j, words):
        rightMatcher = SeqMatcher(self.machers[j+1:])
        track = matcher.track[:]
        track.reverse()
        j = len(track)-1
        for i in track:
            newwords = words[i:]
            r = rightMatcher(newwords)
            if r != -1 :
                self.catch.extend(matcher.catch[:j])
                matcher.matchTime = j
                self.catch.extend(rightMatcher.catch)
                return i + r
            j-=1
        return -1
            
          
    def output(self):      
        result = []
        for mathcer in self.machers:
            result.extend(mathcer.output())
        return self.outfun(result)
    
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
        
    def output(self): 
        if self.catchMacher is not None:
            result = self.catchMacher.output()
            return result
        else :
            return None

# repreat matcher will not work very well like:
#    sent1 = 'abcabcabcabcde'        
#    match = re.search(r'(abc)*abcd', sent1)

class BaseRepeatMatcher(BaseMatcher):
    def __init__(self, matcher):
        BaseMatcher.__init__(self)
        self.matcher = matcher 
        self.matchTime = 0
        
    def reset(self):
        BaseMatcher.reset(self)
        self.matchTime = 0
        self.matcher.reset() 
        
    def output(self):      
        result = []
        for i in range(self.matchTime):
            result.extend(self.matcher.outfun(self.catch[i]))
        return result
            
class RepeatMatcher(BaseRepeatMatcher):
    
    def __init__(self, matcher, mintimes=0, maxtimes=9999):
        BaseRepeatMatcher.__init__(self, matcher)   
        self.minTimes = mintimes
        self.maxTimes = maxtimes         
    
    def match(self, words): 
        self.reset()      
        last = 0 
        self.track=[0]
       
        while self.matchTime < self.minTimes :            
            i = self.matcher(words)
            if i!=-1 :
                self.catch.append(self.matcher.catch)
                words = words[i:]
                self.matchTime +=1
                last += i
                self.track.append(last)
            else:
                break
        if self.matchTime < self.minTimes:
            return -1
        
        while self.matchTime < self.maxTimes : 
            i = self.matcher(words)
            if i!=-1 :
                self.catch.append(self.matcher.catch)
                self.matchTime +=1
                words = words[i:]
                last += i
                self.track.append(last)
            else:
                break
            
        return last


class QuestionMatcher(RepeatMatcher):    
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher, mintimes=0, maxtimes=1)
        
class StarMatcher(RepeatMatcher):
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher)
       
class PlusMatcher(RepeatMatcher):
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher, mintimes=1) 
    
    