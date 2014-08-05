# -*- coding: utf-8 -*-
"""
Created on Mon Aug 04 23:17:48 2014

@author: dlmu__000
http://morepypy.blogspot.com/2010/05/efficient-and-elegant-regular.html
"""

def match(re, s):
    if not s:
        return re.empty
    # shift a mark in from the left
    result = re.shift(s[0], True)
    for c in s[1:]:
        # shift the internal marks around
        result = re.shift(c, False)
    re.reset()
    return result

class Regex(object):
    def __init__(self, empty):
        # empty denotes whether the regular expression
        # can match the empty string
        self.empty = empty
        # mark that is shifted through the regex
        self.marked = False

    def reset(self):
        """ reset all marks in the regular expression """
        self.marked = False

    def shift(self, c, mark):
        """ shift the mark from left to right, matching character c."""
        # _shift is implemented in the concrete classes
        marked = self._shift(c, mark)
        self.marked = marked
        return marked
        
class Char(Regex):
    def __init__(self, c):
        Regex.__init__(self, False)
        self.c = c

    def _shift(self, c, mark):
        return mark and c == self.c
        
class Epsilon(Regex):
    def __init__(self):
        Regex.__init__(self, empty=True)

    def _shift(self, c, mark):
        return False
        
class Binary(Regex):
    def __init__(self, left, right, empty):
        Regex.__init__(self, empty)
        self.left = left
        self.right = right

    def reset(self):
        self.left.reset()
        self.right.reset()
        Regex.reset(self)

class Alternative(Binary):
    def __init__(self, left, right):
        empty = left.empty or right.empty
        Binary.__init__(self, left, right, empty)

    def _shift(self, c, mark):
        marked_left  = self.left.shift(c, mark)
        marked_right = self.right.shift(c, mark)
        return marked_left or marked_right
        
        
class Repetition(Regex):
    def __init__(self, re):
        Regex.__init__(self, True)
        self.re = re

    def _shift(self, c, mark):
        return self.re.shift(c, mark or self.marked)

    def reset(self):
        self.re.reset()
        Regex.reset(self)
        
        
class Sequence(Binary):
    def __init__(self, left, right):
        empty = left.empty and right.empty
        Binary.__init__(self, left, right, empty)

    def _shift(self, c, mark):
        old_marked_left = self.left.marked
        marked_left = self.left.shift(c, mark)
        marked_right = self.right.shift(
            c, old_marked_left or (mark and self.left.empty))
        return (marked_left and self.right.empty) or marked_right
        
def test1():
   re = Alternative(Alternative(Char('a'), Char('b')), Char('c'))
   print match(re,"a")    
   print match(re,"b")    
   
def test2():
   re = Alternative(Alternative(Char('a'), Char('b')), Char('c'))
   re = Repetition(re)
   print match(re,"ab")    
   print match(re,"bd")  

test2()    
        
