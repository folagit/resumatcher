# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:24:09 2014

@author: dlmu__000

"""

from prettytable import PrettyTable
from tokenfilter import *

class JobSentence():
    puncts = [".", ",", ";","?", "!", ":", "(", ")" ,"-","+" ,"/" ]
    tagDict = {  }    
    
    def __init__(self, words):
        self.words = words
        self.lower_words = [word.lower() for word in self.words]
        self.tags = [None] * len(self.words)
        self._firstTag()
        
    def _firstTag(self):         
        
        i = 0       
        while i < len(self.words):
            word = self.words[i]     
            if word in  JobSentence.puncts :
                self.tags[i] = (  word , True )  
          #  if str.isdigit(word) :
            if word.isdigit():
                self.tags[i] = (  "DIGIT" , True ) 
            elif JobSentence.tagDict.has_key(word):
                self.tags[i] = ( JSentence.tagDict[word], True )
            i+=1
    
    
    def findUntaggedRanges( self ):
        ranges = []
        i = 0
        word_len = len(self.words)
        while i  < word_len :
        #    print "i=", i
            if self.tags[i] != None :
                i += 1
            else:
                j  =  i                
                while j < word_len and  self.tags[j] == None:
                    j+=1
             #       print "j=", j
                if  self.tags[j-1] == None :
                    ranges.append( (i , j-i ) )
                    i = j + 1
                if j == word_len :
                    break
                
        return ranges                
         
           
    def labelWithTuple(self, labelTuple):
        toekens , label =  labelTuple  
        has_tagged = True
        while has_tagged:
            has_tagged = False
            # after tag one label, reset ranges
            ranges = self.findUntaggedRanges()
     #       print "ranges=", ranges
            for untagged in ranges:
                i = findTokenSquence(toekens, self.words, scope = untagged )
            # here only find once in one range            
     #           print untagged , i 
                if i != -1 :
                     self.tags[i] = (label, True)
                     j=1 
                     while j < len(toekens) :
                         self.tags[i+j] = (label, False)
                         j += 1        
                     has_tagged = True
                     break
                 
    def getLabeledRange(self):        
        array = []        
        i = 0
        tag = self.tags[i] 
        if tag is None:
            label = "$NA$"
        else:    
            label = tag[0]         
        item = [ label, i , None ]
        
        i = 1 
        while i < len(self.tags):
            tag = self.tags[i] 
            if tag is None:
                label = "$NA$"
                start = True  
            else:    
                label , start = tag  
            if start :
                item[2] = i
                array.append(item)
                item = [ label, i, None ]            
            i += 1
            
        item[2] = i
        array.append(item)
        self.labeledArray = array
        return array
        
    def getOnto(self, ontoDict, label):      
        if ontoDict.has_key(label):
            onto = ontoDict[label]
        else :
            onto = label
        return onto        
    
    def getLabeledArray(self, ontoDict):        
        array = []        
        i = 0
        tag = self.tags[i] 
        if tag is None:
            label = "$NA$"          
        else:    
            label = tag[0]          
       
        item = [ self.getOnto(ontoDict,label), label, [self.words[i]] ] 
        
        i = 1 
        while i < len(self.tags):
            tag = self.tags[i] 
            if tag is None:
                label = "$NA$"
                start = True  
            else:    
                label , start = tag  
                
            if start :                
                array.append(item)
                item = [ self.getOnto(ontoDict,label) , label, [self.words[i]] ] 
            else :
                item[2].append(self.words[i])         
            i += 1            
       
        array.append(item)
        self.labeledArray = array
        return array
        
    def printLabeledArray(self):
        list0 = []
        list1 = [] 
        list2 = []
        for item in self.labeledArray :
            onto , label , words = item    
            list0.append(onto)
            list1.append(label)
            list2.append(words)
         
        x = PrettyTable()
        x.add_row(list0)
        x.add_row(list1)
        x.add_row(list2)
        return x                
        
    def printSentenct(self):
       
      lists = [0] * 3 
      lists[0] = self.words
      lists[1] = [ "None" if tag is None else tag[0] for tag in self.tags ] 
      lists[2] = [ " " if tag is None else str(tag[1]) for tag in self.tags ] 
      
      x = PrettyTable()
      x.add_row(lists[0])
      x.add_row(lists[1])
      x.add_row(lists[2])
      return x
   
def test_sentence1():
    words = "I am ok or not , with you and me .".split()  
    
    sent = JSentence(words)
 #   print sent.tags
    sent.labelWithTuple(( ["or", "not", ",", "with"] , "AAAA" ))
    print sent.tags  
    
def test_sentence2():
    words = "I am ok or not , am ok and am ok . and  am ok".split()  
    
    sent = JSentence(words)
 #   print sent.tags
  #  sent.labelWithTuple(( ["am", "ok"] , "AAAA" ))
  #  sent.labelWithTuple(( ["am" ] , "AAAA" ))
    sent.labelWithTuple(( ["am", "ok" , "and"] , "AAAA" ))
    print sent.tags  
  

def test_sentence3():
   words = ['B.S.', 'degree', 'in', 'Computer', 'Science', 'required']
   sent = JSentence(words)
   sent.labelWithTuple(( ["B.S."] , "AAAA" ))
   print sent.printSentenct()           
   print sent.tags 
                
def main(): 
   test_sentence3()
 #  beforeDegree()
    
if __name__ == "__main__": 
    main() 