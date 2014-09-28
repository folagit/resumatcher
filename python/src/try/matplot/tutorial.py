# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 16:12:01 2014

@author: dlmu__000
"""

import matplotlib.pyplot as plt
import numpy as np

plt.plot([-3,4,3,8])
plt.ylabel('some numbers')
plt.show()

plt.plot([1,2,3,4], [1,4,9,16], 'ro')
plt.plot([1,2,3,4], [1,4,9,16], 'bo')
plt.axis([0, 6, 0, 20])
plt.show()

# evenly sampled time at 200ms intervals
t = np.arange(0., 5., 0.4)
print t

# red dashes, blue squares and green triangles
plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
plt.show()

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10 )
print x 
# the histogram of the data
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()