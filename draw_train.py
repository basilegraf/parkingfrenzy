#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 11:25:56 2020

@author: basile
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.collections import PatchCollection

from train_anim import train


fig, ax = plt.subplots()
ax.set_aspect(aspect='equal', adjustable='box')
ax.set_xlim([-.3,3.8])
ax.set_ylim([-.6,2.5])
ax.axis('off')

L = [1,1,1,1]
width = 0.8

tr = train(ax, width, L)

a = [np.pi/12, np.pi/4, np.pi/7, np.pi/3]
x0 = 0
y0 = 0
xy = np.array([[x0,y0]])
for k in range(len(a)):
    xy = np.concatenate((
        xy,
        xy[-1] + L[k]*np.array([[np.cos(a[k]), np.sin(a[k])]])
         ))

tr.place(xy[:,0], xy[:,1])
tr.alpha(0.2)

ax.plot(xy[:,0], xy[:,1], 'ko-')


for k in range(len(xy[:,0])):
    txt=plt.text(  # position text relative to Figure
        xy[k,0]+0.5, xy[k,1],'$(x_%d, y_%d)$' % (k+1,k+1),
        ha='center', va='center',
        fontsize=12, 
        color = 'black',
        usetex=True)
    ax.add_artist(txt)

fig.tight_layout()
fig.show()