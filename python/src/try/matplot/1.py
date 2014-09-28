# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 16:04:22 2014

@author: dlmu__000
"""

import random
import matplotlib.pyplot as plt
x = random.sample(range(1000), 100)
xbins = [0, len(x)]
#plt.hist(x, bins=xbins, color = 'blue') 
#Does not make the histogram correct. It counts the occurances of the individual counts. 
x = [10,20,30,40]
plt.plot(x)
#plot works but I need this in histogram format
plt.bar(range(0,100), x)
plt.show()