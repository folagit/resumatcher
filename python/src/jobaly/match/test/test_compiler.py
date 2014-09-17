
import sys
sys.path.append("..") 
from matchercompiler import MatcherCompiler
import unittest

tokens1 = ["aaa","bbb","ccc","ddd"]
tokens2 = ["aaa","bbb","aaa","bbb","aaa","bbb","aaa","bbb","ccc","ddd"]
tokens3 = [ "bachelors" ,  "Degree"]

class TestCompiler1(unittest.TestCase): 
    
    def setUp(self):
        self.compiler = MatcherCompiler()
    
    def test1(self):       
       matcher = self.compiler.parse("aaa")
       self.assertEqual(str(matcher), "'aaa'")
       self.assertEqual( matcher(tokens1), 1 )
       self.assertEqual( matcher.catch, ["aaa"] )
       self.assertEqual( matcher.output(), ["aaa"] )
       
    def test2(self):       
       matcher = self.compiler.parse("aaa bbb")
       self.assertEqual( str(matcher), "<Seq:'aaa','bbb'>")
       self.assertEqual( matcher(tokens1), 2 ) 
       self.assertEqual( matcher.catch, ["aaa", "bbb"] )
       self.assertEqual( matcher.output(),  ['aaa', 'bbb'] )
     
    def test3(self):   
         matcher = self.compiler.parse("DE_LEVEL (, DE_LEVEL)* (OR DE_LEVEL)? DEGREE")
         print str(matcher)
         self.assertEqual( matcher(tokens3), 2 ) 
     
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCompiler1)
    unittest.TextTestRunner(verbosity=2).run(suite)