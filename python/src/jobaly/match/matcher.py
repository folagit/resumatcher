# -*- coding: utf-8 -*-
"""
Created on Thu Aug 07 23:05:14 2014

@author: dlmu__000
"""
# such matcher how to handle repeat? 

import copy

class BaseMatcher:    
   
    def __init__(self, catchfun=lambda x:x , outfun=lambda x: x):
        self.catch = []  
        self.catchfun = catchfun
        self.outfun = outfun
        self.found = None
        self.refNum = 0
        self.outlist = [] 
        self.matchNum = 0
        
    def setCatchFun(self, catchfun):
        self.catchfun = catchfun
        
    def setOutFun(self, outfun):
        self.outfun = outfun
    
    def reset(self):
        self.catch = []   
        self.outlist = [] 
        self.found = None
        
    def match(self, tokens):
        return  -1
        
    def getOutList(self, n=None):
        return self.outlist        
        
    def addOutput(self, matcher):        
            self.outlist.extend(matcher.getOutList())
        
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
            
    def output(self):  
        return self.outfun(self.getOutList())
        
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

class UnitMatcher(BaseMatcher):
   def __init__(self,  catchfun=lambda x:x , outfun=lambda x: x):        
        BaseMatcher.__init__(self, catchfun, outfun) 


class DotMatcher(UnitMatcher):    
    def __init__(self,  catchfun=lambda x:x , outfun=lambda x: x):        
        BaseMatcher.__init__(self, catchfun, outfun) 
        
    def match(self, words):
        self.reset()
        if len(words) < 1:
            return  -1 
      
        self.catch.append(words[0])
        self.outlist = self.catchfun(self.catch) 
        return  1
        
    def __repr__(self):
        return '<.>'

class UnitTokenMatcher(UnitMatcher):
    
    def __init__(self, token, catchfun=lambda x:x , outfun=lambda x: x):        
        UnitMatcher.__init__(self, catchfun, outfun)
        self.token = token      
    
    @staticmethod    
    def getWord(item):
        return item
       
    def match(self, words):
        self.reset()
        if len(words) < 1:
            return  -1 
        if self.token  == self.getWord(words[0]):
            self.catch.append(words[0])
            self.outlist = self.catchfun(self.catch) 
            return 1
        else:
            return -1      
            
    def __repr__(self):
        return '<Tok:'+self.token+'>'
        
class TokenMatcher(UnitMatcher):
    
    def __init__(self, tokens, catchfun=lambda x:x , outfun=lambda x: x):        
        UnitMatcher.__init__(self, catchfun, outfun)
        if type(tokens) is str:
            self.tokens = [tokens]
        elif type(tokens) is list:
            self.tokens = tokens        
    
    @staticmethod    
    def getWord(item):
        return item   
       
    def match(self, words):
        self.reset()
        if len(words) < len(self.tokens):
            return  -1        
        i = 0 
        while i<len(self.tokens) and \
            self.tokens[i] == self.getWord(words[i]):
            self.catch.append(words[i])
            i += 1
        
        if i == len(self.tokens):
           self.outlist = self.catchfun(self.catch) 
           return  i 
        else:
           return  -1

class CompMatcher(BaseMatcher): 
    
    def __init__(self, matchers=None , catchfun=lambda x:x , outfun=lambda x: x):
         BaseMatcher.__init__(self, catchfun,outfun )
         self.matchers = []
         if matchers == None :
             pass
         elif type(matchers) is list:
             for matcher in matchers:
                 self.append(matcher)
         elif isinstance(matchers, BaseMatcher ):
             self.append(matchers)
    
    def append(self, matcher):
        if matcher.refNum == 0 :            
            self.matchers.append(matcher)
            matcher.refNum += 1
        else :
            matcher2 =  copy.deepcopy(matcher)
            self.matchers.append(matcher2)
            matcher2.refNum = 1

    def extend(self, matchers):
        self.matchers.extend(matchers)          
     
    def reset(self):
        BaseMatcher.reset(self)
        for catcher in self.matchers:
            catcher.reset()
         
class SeqMatcher(CompMatcher):
    
    def __init__(self, matchers=None, catchfun=lambda x:x , outfun=lambda x: x):
         CompMatcher.__init__(self, matchers, catchfun, outfun )
    
    def match(self, words):
        self.reset()
        i = 0
        j = 0  # index of matcher        
        last = 0
        while j<len(self.matchers) and ( i != -1):
            matcher = self.matchers[j]
            i =  matcher(words)
            if i != -1:
                if not isinstance(matcher, RepeatMatcher) or \
                    j==len(self.matchers)-1 or i==0:
                   self.catch.extend(matcher.catch) 
                   words = words[i:]
                   j +=1  
                   last += i
                   self.addOutput(matcher) 
                else :                  
                   i = self.matchWithRepeat(matcher, j,  words) 
                   if i != -1:
                       last += i
                       return last
               
        if j == len(self.matchers):
            return  last
        else:
            return  -1
     
    def matchWithRepeat(self, matcher, j1, words):
        rightMatcher = SeqMatcher(self.matchers[j1+1:])
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
                self.matchers[j1+1:] = rightMatcher.matchers
                self.outlist.extend(matcher.getOutList(j)) 
                self.outlist.extend(rightMatcher.outlist) 
                return i + r
            j-=1
        return -1
        
    def __repr__(self):  
        s=""
        for m in self.matchers:
            s+= ","+str(m)
        if len(s)>0:
            s=s[1:]
        return '<Seq:'+s+'>'
    
class AlternateMatcher(CompMatcher):
    
    def __init__(self, matchers=None):
         CompMatcher.__init__(self, matchers)
         
    def match(self, words):
        self.reset()
       
        j = 0  # index of matcher         
        while j<len(self.matchers) :
            matcher = self.matchers[j]
            i =  matcher(words)
            if i != -1:
               self.catch = matcher.catch
               self.catchmatcher = matcher
               self.addOutput(matcher) 
               return i
            else:
               j+=1
               
        if j == len(self.matchers):
            return  -1
            
    def reset(self):
        CompMatcher.reset(self)
        self.catchmatcher = None 
        
    def __repr__(self):  
        s=""
        for m in self.matchers:
            s+= ","+str(m)
        if len(s)>0:
            s=s[1:]
        return '<Alt:'+s+'>'    

# repreat matcher will not work very well like:
#    sent1 = 'abcabcabcabcde'        
#    match = re.search(r'(abc)*abcd', sent1)

class BaseRepeatMatcher(BaseMatcher):
    def __init__(self, matcher):
        BaseMatcher.__init__(self)
        if matcher.refNum == 0 :
            self.matcher = matcher 
            matcher.refNum  += 1
        else :
            matcher2 = copy.deepcopy(matcher)
            matcher2.refNum = 1
            self.matcher = matcher2 
        self.matchTime = 0
        self.outCache = []
        
    def reset(self):
        BaseMatcher.reset(self)
        self.matchTime = 0
        self.matcher.reset() 
        self.outCache = []
  
            
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
                self.outCache.append ( self.matcher.outlist ) 
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
                self.outCache.append (self.matcher.outlist) 
            else:
                break
            
        return last
        
    def getOutList(self, n=None):
        if n is None:
            n = self.matchTime
        for item in self.outCache[:n]:
            self.outlist.extend(item)
        return self.outlist        

class QuestionMatcher(RepeatMatcher):    
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher, mintimes=0, maxtimes=1)
    def __repr__(self):        
        return '<?:'+str(self.matcher)+'>'
        
class StarMatcher(RepeatMatcher):
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher)  
    def __repr__(self):        
        return '<*:'+str(self.matcher)+'>'
       
class PlusMatcher(RepeatMatcher):
    def __init__(self, matcher):
        RepeatMatcher.__init__(self, matcher, mintimes=1) 
    def __repr__(self):        
        return '<+:'+str(self.matcher)+'>'
    