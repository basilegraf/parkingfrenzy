#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:04:22 2020

@author: basile
"""

import trailer_poly as tp
import scipy.interpolate as interp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Use qt for animations
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass


n = 5


v = np.array([1e6])
for k in range(n):
    v = np.concatenate((v,-v))
v = np.concatenate(([0], v, [0]))
    
# c = v
# for k in range(n+1):
#     c = np.cumsum(c)
#c = np.concatenate((np.zeros(n+1, dtype='int'), c))

t = np.linspace(0, 1, len(v) + 1)
tt = np.linspace(0, 1, 10*len(v) + 1)

b = interp.BSpline(t,v,0)
bb=[b]
for k in range(1, n + 2):
    bb.append(bb[-1].antiderivative(1))
    #bb[-1].c *= max(n + 1 -k, 1)
    
    
if False:
    for k in range(len(bb)):
        h=plt.figure
        plt.plot(tt, bb[k](tt))
        plt.show()
    
Y = np.zeros((len(bb), len(tt)))
for k in range(len(bb)):
    Y[len(bb)-1-k,:] = bb[k](tt)
    
lx = .7
X = np.zeros((len(bb), len(tt)))
X[0,:] = np.linspace(0,lx,len(tt))
X[1,:] = lx * np.ones(len(tt))

TX = 0*X
TY = 0*Y
L = 0.1 * np.ones(len(bb)-1)
for k in range(len(tt)):
    TX[:,k], TY[:,k], vx, vy = tp.trailers_positions_r(
        tp.derivatives_to_poly(X[:,k]), 
        tp.derivatives_to_poly(Y[:,k]), L)
    
fig, ax = plt.subplots(1,1)
ax.plot(TX.transpose(),TY.transpose())
ax.axis('equal')
plt.show()




class animTrailers:
    def __init__(self, TX, TY):
        self.fig, self.ax = plt.subplots()
        self.TX = TX
        self.TY = TY
        self.frames = range(TX.shape[1])
        
    def initAnim(self):
        self.ax.clear()
        self.ln, = self.ax.plot(self.TX[:,0], self.TY[:,0])
        self.ax.set_aspect(aspect='equal', adjustable='box')
        self.ax.set_xlim(left=0, right=1.5)
        self.ax.set_ylim(bottom=0, top=1)
        #self.ax.set_xbound(lower=-5, upper=5)
        #self.ax.set_ybound(lower=-0.5, upper=8)
        self.ax.grid(b=True)
        
    def updateTrailers(self, frame):
        self.ln.set_xdata(self.TX[:, -frame])
        self.ln.set_ydata(self.TY[:, -frame])
        #self.ln, = self.ax.plot(self.TX[:,frame], self.TY[:,frame])
       
    def anim(self):
        return FuncAnimation(self.fig, self.updateTrailers, self.frames, init_func=self.initAnim, blit=False, repeat_delay=1000, interval=50)
        

anim = animTrailers(TX, TY)
aa = anim.anim()

# if saveAnimation:
#     aa.save('beforeOptim.gif', writer='imagemagick', fps=25)