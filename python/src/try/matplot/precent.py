# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 16:57:51 2014

@author: dlmu__000
"""
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

x = [1,    2,    3,    4,    5,    6]
y = [0.66, 0.79, 0.87, 0.89, 0.92, 0.94]

formatter = FuncFormatter(to_percent)
# Set the formatter
plt.gca().yaxis.set_major_formatter(formatter)

#plt.plot(x, y, 'bo')
plt.plot(x, y)
plt.plot(x, y, 'r^')
plt.axis([0, 7, 0.5,1])
plt.grid(True)
plt.xlabel('Pattern Number')
plt.ylabel('Accuracy')
plt.title('Accuracy of Degree Extraction')

plt.show()