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
import numpy.matlib
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
m = 2
p = n+m
tMax = 1
lx = 1
ly = 1
L = 1 * np.ones(n)
tt=np.linspace(0,tMax,1000)

# n+m-th  spline coeff
beu = tMax * np.ones(n+m)
t = np.concatenate((np.zeros(n+m), np.linspace(0,tMax,p+1), beu))
c = np.concatenate((np.zeros(n+m), ly*np.ones(p), ly*np.ones(n+m)))

b = interp.BSpline(t, c, n+m)

plt.plot(tt, b.derivative(0)(tt))
plt.grid(True)
    





bb=[b]
for k in range( n):
    bb.append(bb[-1].derivative(1))
    bb[-1].c /= max(1, k)
    

    
    
if False:
    for k in range(len(bb)):
        h=plt.figure
        plt.plot(tt, bb[k](tt))
        plt.show()
    
Y = np.zeros((len(bb), len(tt)))
for k in range(len(bb)):
    Y[k,:] = bb[k](tt)
    

X = np.zeros((len(bb), len(tt)))
X[0,:] = np.linspace(0,lx,len(tt))
X[1,:] = lx * np.ones(len(tt))

TX = 0*X
TY = 0*Y
for k in range(len(tt)):
    TX[:,k], TY[:,k], vx, vy = tp.trailers_positions_r(
        X[:,k], 
        Y[:,k], L)
    
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
        self.ax.plot(TX.transpose(),TY.transpose())
        self.ln, = self.ax.plot(self.TX[:,-1], self.TY[:,-1], 'o-',linewidth=3, color='black')
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
        
nRep = 3
TXX = np.concatenate((
    np.matlib.repmat(TX[:,:1],1,nRep),
    TX,
    np.matlib.repmat(TX[:,-1:],1,nRep)), axis=1)
TYY = np.concatenate((
    np.matlib.repmat(TY[:,:1],1,nRep),
    TY,
    np.matlib.repmat(TY[:,-1:],1,nRep)), axis=1)
anim = animTrailers(TXX, TYY)
aa = anim.anim()

# if saveAnimation:
#     aa.save('beforeOptim.gif', writer='imagemagick', fps=25)