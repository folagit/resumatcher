# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 12:22:31 2014

@author: dlmu__000
"""

class Foo(object):
     pass
 
foo = Foo()
foo.a = 3

Foo.b = property(lambda self: self.a + 1)

print "foo.a =", foo.a
print "foo.b =", foo.b

foo.a = 10
print "foo.a =", foo.a
print "foo.b =", foo.b
