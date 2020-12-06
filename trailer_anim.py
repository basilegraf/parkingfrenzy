#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:04:22 2020

@author: basile
"""
import math
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


n = 4
m = 3
lx = 1
ly = .3
L = 0.3 * np.ones(n)

# n-th derivative spline coeff
v = np.array([1.0])
for k in range(n + m - 1):
    v = np.concatenate((v,-v))
v = np.concatenate(([0], v, [0]))
    

# c = v
# for k in range(n+1):
#     c = np.cumsum(c)
#c = np.concatenate((np.zeros(n+1, dtype='int'), c))

t = np.linspace(0, 1, len(v) + 1) # knots
b = interp.BSpline(t,v,0)
endVal = b.antiderivative(n + m)(1)
b.c *= (ly / endVal)

# v /= (t[1]-t[0])**(n) * math.factorial(n) * vv[-1]

tt = np.linspace(0, 1, 10*len(v) + 1)

b = interp.BSpline(t,v,0)
bb=[b.antiderivative(m)]
for k in range(1, n + 1):
    bb.append(bb[-1].antiderivative(1))
    #bb[-1].c *= max(n + 1 -k, 1)
    
fac = ly / bb[-1].c[-1]
for k in range(n):
    bb[k].c *= fac
    
    
if False:
    for k in range(len(bb)):
        h=plt.figure
        plt.plot(tt, bb[k](tt))
        plt.show()
    
Y = np.zeros((len(bb), len(tt)))
for k in range(len(bb)):
    Y[len(bb)-1-k,:] = bb[k](tt)
    

X = np.zeros((len(bb), len(tt)))
X[0,:] = np.linspace(0,lx,len(tt))
X[1,:] = lx * np.ones(len(tt))

TX = 0*X
TY = 0*Y
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
        self.ax.set_xlim(left=np.min(self.TX), right=np.max(self.TX))
        self.ax.set_ylim(bottom=np.min(self.TY), top=np.max(self.TY))
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