# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:34:36 2015

@author: Administrator
"""
import numpy as np

data = np.loadtxt('data.txt', delimiter=',', usecols=(0,1,2,3,4,5))
res = np.loadtxt('data.txt', delimiter=',', usecols=(6,), dtype=str)

weather = np.loadtxt('weather.txt', delimiter=',', usecols=(0,1,2,3), dtype=str)
feel = np.loadtxt('weather.txt', delimiter=',', usecols=(4,), dtype=str)