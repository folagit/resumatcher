# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 15:34:27 2015

@author: dlmu__000
"""
import re

matrix = [[1, 0.1981, 0.2087, 0.2439, 0.0665, 0.019, 0.0231, 0.0422, 0.0121, 0.0045], 
          [0.1981, 1, 0.0979, 0.1328, 0.0439, 0.0142, 0.0266, 0.0344, 0.0035, 0.0036], 
          [0.2087, 0.0979, 1, 0.3569, 0.0473, 0.0175, 0.023, 0.0375, 0.0048, 0.002], 
          [0.2439, 0.1328, 0.3569, 1, 0.0537, 0.0153, 0.0181, 0.0488, 0.0055, 0], 
          [0.0665, 0.0439, 0.0473, 0.0537, 1, 0.0502, 0.0292, 0.0339, 0.0523, 0.0147], 
          [0.019, 0.0142, 0.0175, 0.0153, 0.0502, 1, 0.1333, 0.0231, 0.0032, 0.0239], 
          [0.0231, 0.0266, 0.023, 0.0181, 0.0292, 0.1333, 1, 0.0257, 0.0029, 0.0361], 
          [0.0422, 0.0344, 0.0375, 0.0488, 0.0339, 0.0231, 0.0257, 1, 0.006, 0.0024], 
          [0.0121, 0.0035, 0.0048, 0.0055, 0.0523, 0.0032, 0.0029, 0.006, 1, 0],
          [0.0045, 0.0036, 0.002, 0, 0.0147, 0.0239, 0.0361, 0.0024, 0, 1]]

terms=["javascript", "jquery", "html", "css", "java", "python", "ruby", "mysql", "jdbc" , "cpp"  ]
posmap = {}
for i in range(0,len(terms)):
    posmap[terms[i]] = i   

f = open('human.csv','r')
line1 = f.readline().lower()
line1 = re.sub("c\+\+", "cpp", line1)
      
line2 = f.readline()
tokens = line1.split(',')
values = [float(value) for value in line2.split(',')]
pairs = [ token.split(":") for token in tokens]
pairs = [ [pair[0].strip(),pair[1].strip() ] for pair in pairs]
humans = [ [pairs[i][0], pairs[i][1], values[i]] for i in range(0, len(pairs))]

matrixhuman = [[5.0 for x in range(10)] for x in range(10)] 
import math
for pair in humans:
    x = posmap.get(pair[0])
    y = posmap.get(pair[1])    
    matrixhuman[x][y] = pair[2]
    matrixhuman[y][x] = pair[2]
 #   print pair[0], pair[1], pair[2], x, y 
def calNdcg(x):
     
    human = [  [terms[i], matrixhuman[x][i]] for i in range(0,10) ]
    human =   sorted(human, key=lambda tup: tup[1], reverse= True)
    dis = [  [terms[i], matrix[x][i]] for i in range(0,10) ]
    dis =   sorted(dis, key=lambda tup: tup[1], reverse= True)
    idcg = 0
    dcg  = 0
    for i in range(0,10):
        idcg += (2**human[i][1] - 1 ) / (math.log(2+i,2))        
        y = posmap.get(dis[i][0])
      #  print dis[i][0] , y , matrixhuman[x][y]
        dcg += (2**matrixhuman[x][y] - 1 ) / (math.log(2+i,2))
  #  print human
  #  print dis
   # print dcg, idcg, dcg/idcg
    
    return dcg/idcg

ndcgs = [ [terms[i], calNdcg(i)] for i in range(0,10)]
print ndcgs
