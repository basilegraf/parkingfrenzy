#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 14:52:48 2020

@author: basile
"""
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from matplotlib.collections import PatchCollection


# degree to load from result file
n = 5

# load data
fileName = "data/SXSY_n%d.npy" % n
with open(fileName, 'rb') as f:
    SX = np.load(f)
    SY = np.load(f)
    f.close()
    
    
    
fig, ax = plt.subplots()
ax.plot(SX[-1::-1,:].transpose(), SY[-1::-1,:].transpose(), zorder=-1000, alpha = 0.7)