import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import re
import jobaly.utils as utils


class TfGetter():
    
     def __init__(self, _stopwords=None  ):       
        if _stopwords is None :
            _stopwords = utils.loadArrayFromFile("jobaly_stopwords.txt")
     #   print _stopwords
        TfGetter.stopwords = set(_stopwords)
        TfGetter.term_num_docs = {}    
        
     def getTokens(self, content):
         tokens =   re.split(' |,|;|\n|!|\r|\||\-|\/|\\\\',content)
         tokens =   self.filterTokens(tokens) 
         return tokens
   
     def getTf(self, tokens):    
        term_freq = {}
        for token in tokens:
            if term_freq.has_key(token):
                term_freq[token] += 1
            else :
                term_freq[token] = 1           
        
        return term_freq          
    
     def filterTokens(self, tokens):
          new_tokens = []
          for token in tokens:
              token = token.lower()
        #     print   self.needToBeFilter(token)
              if len(token)> 0:
                  token = re.sub('\.|\)|\(|\:|\-|\_|\?|\!|\>|\<|\"|\[|\]|\~|\'|\*|\=|\{|\}|\$', '', token)
                
                  if len(token)> 0 and (not token in TfGetter.stopwords) :
                      new_tokens.append(token)
          return new_tokens

     
def main():

    tfgetter =  TfGetter()   
    print tfgetter.getTf("the book is pretty good good one book".split())
    
        
if __name__ == "__main__": 
    main()  
