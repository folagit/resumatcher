# -*- coding: utf-8 -*-
"""
Created on Fri Apr 04 20:34:56 2014

@author: dlmu__000
"""

#!/usr/bin/env python
import Queue
import threading
import sys
import time
  
hosts = ["A","B","C","D","E","F","G","H"]
hosts = range(100,110) 
  
queue = Queue.Queue()
lock = threading.Lock()
  
class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
      threading.Thread.__init__(self)
      self.queue = queue
      
    def run(self):
        while (not self.queue.empty()):
            self.printOne()
    
    def printOne(self):
       url = self.queue.get()
     #  print "url=", url 
       lock.acquire(True)
       print
       print "size=" , self.queue.qsize(), "#"       
    #   time.sleep(1)           
       lock.release()
           
       if url == "C" :
           print "C"
       else :   
           for i in range(1,20) :
            #   with lock:
                   sys.stdout.write( str(url) )
                   sys.stdout.write(" " )
           print  " "
           
       self.queue.task_done()       
       
start = time.time()      
        
def main():
   

    #populate queue with data   
   for host in hosts:
       queue.put(host)    
   print queue
    #spawn a pool of threads, and pass them queue instance 
   tl = []   
   
   for i in range(3):
      t = ThreadUrl(queue)
      t.setDaemon(True)
      t.start()
      tl.append(t)
      
    
 #  t.join() 
   
   
       #wait on the queue until everything has been processed     
   queue.join()
     
   print "main thread finish" 
    
main()
print "Elapsed Time: %s" % (time.time() - start)