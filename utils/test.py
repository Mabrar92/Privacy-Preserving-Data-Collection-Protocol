# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 00:02:28 2019

@author: Abrar
"""
j=0
listt=[]

for i in range(1,100):
    if i % 3 == 0 or i % 5 == 0:
        listt.append(i)
        j=j+1
        
print(listt)
print(len(listt))