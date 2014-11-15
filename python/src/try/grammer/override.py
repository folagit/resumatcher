# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 22:32:08 2014

@author: dlmu__000
"""

class A(object):
   def method1(self):
      print "aaaa"
        
class B(A):
   def method1(self):
      print "bbbb"
      super(B, self).method1()
      print "bbbb"
        
#a = A()
#a.method()
b = B()
b.method1()

import datetime

class Logger(object):
    def log(self, message):
        print message

class TimestampLogger(Logger):
    def log(self, message):
        message = "{ts} {msg}".format(ts=datetime.datetime.now().isoformat(),
                                      msg=message)
        super(TimestampLogger, self).log(message)
        
t = TimestampLogger()
t.log('hi!')