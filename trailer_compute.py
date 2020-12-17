#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 17:04:22 2020

@author: basile
"""
import time
import math
import trailer_power_series as tp
import scipy.interpolate as interp
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from matplotlib.animation import FuncAnimation

# Use qt for animations
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass


n = 15 # number of links (trailers)
m = 2 # additional smoothness
p = n+m # spline order 
sMax = 1 # path parameter goes from 0 to sMax
lx = 1 # distance covered in x while maneuvring
ly = 1 # distance covered in y while maneuvring
L = 1 * np.ones(n) # link lengths


# n+m-th  spline coeff
knots = np.concatenate((np.zeros(n+m), np.linspace(0,sMax,p+1), sMax * np.ones(n+m)))
c = np.concatenate((np.zeros(n+m), ly*np.ones(p), ly*np.ones(n+m)))

# B-Spline for the sigmoid
b = interp.BSpline(knots, c, n+m)

# show the sigmoid function
sVals = np.linspace(0,sMax,1000)
plt.plot(sVals, b.derivative(0)(sVals))
plt.grid(True)

# spline derivatives 0 to n
bb=[b]
for k in range(n):
    bb.append(bb[-1].derivative(1))
    bb[-1].c /= max(1, k)
    
    
# compute derivative of (n-1)-th link position w.r.t. to path parameter s 
def pathDerivative(sIn):
    s = max(0, min(sIn, sMax))
    x = np.zeros((len(bb)))
    x[0] = s
    x[1] = lx / sMax     # x 1st derivative
    y = np.zeros((len(bb)))
    for k in range(len(bb)):
        y[k] = bb[k](s)
    sx, sy, vx, vy = tp.trailers_positions_r(x, y, L)   
    return 1.0 / np.sqrt(vx[-1]**2 + vy[-1]**2)    


# Solve ode to get s(t) such that (n-1)-th link speed is constant

# first solve with "low" accuracy to determine the (n-1)-th path length
tSpan = [0.0, 1.0e6]
s0 = [0]
fInt = lambda tv, sv : pathDerivative(sv)
fEvent = lambda tv, sv : sv[0] - sMax
fEvent.terminal = True

print("Start computing path length")
tComp = time.time()
ivpSol = integrate.solve_ivp(fInt, tSpan, s0, events = fEvent, rtol=1.0e-6, atol=1.0e-6)
tComp = time.time() - tComp
sPathMax = ivpSol.t[-1]
print("Path length = %f, computation time = %f" % (sPathMax, tComp))

# Recompute path by requiring evenly sampled (in time) path postions
tSpan = [0, 2.0 * sPathMax]
dl = 0.05 * np.sqrt(lx**2 + ly**2)
tEval = np.linspace(0, tSpan[1], int(round(tSpan[1] / dl)))
x0 = [0]
fInt = lambda tt, xx : pathDerivative(xx)
fEvent = lambda tt, xx : xx[0]-lx
fEvent.terminal = True

print("Start computing path")
tComp = time.time()
ivpSol = integrate.solve_ivp(fInt, tSpan, x0, events = fEvent, rtol=1.0e-6, atol=1.0e-6, t_eval=tEval)#, max_step = 0.01)
tComp = time.time() - tComp
print("Path computation. Computation time = %f" % tComp)



class animTrailers:
    def __init__(self, SX, SY):
        self.fig, self.ax = plt.subplots()
        self.SX = SX
        self.SY = SY
        self.frames = range(SX.shape[1])
        
    def initAnim(self):
        self.ax.clear()
        self.ax.plot(SX.transpose(),SY.transpose())
        self.ln, = self.ax.plot(self.SX[:,-1], self.SY[:,-1], 'o-',linewidth=3, color='black')
        self.ax.set_aspect(aspect='equal', adjustable='box')
        self.ax.set_xlim(left=np.min(self.SX), right=np.max(self.SX))
        self.ax.set_ylim(bottom=np.min(self.SY), top=np.max(self.SY))
        #self.ax.set_xbound(lower=-5, upper=5)
        #self.ax.set_ybound(lower=-0.5, upper=8)
        self.ax.grid(b=True)
        
    def updateTrailers(self, frame):
        self.ln.set_xdata(self.SX[:, -frame])
        self.ln.set_ydata(self.SY[:, -frame])
        #self.ln, = self.ax.plot(self.TX[:,frame], self.TY[:,frame])
       
    def anim(self):
        return FuncAnimation(self.fig, self.updateTrailers, self.frames, init_func=self.initAnim, blit=False, repeat_delay=1000, interval=50)
 
# Remove non-increasing path parameter values and add some zeros and sMax values
# at both ends
idx = np.concatenate(([True], np.diff(ivpSol.y[0,:])>0))
sValues = np.concatenate(([0,0,0], ivpSol.y[0,idx], [sMax,sMax,sMax,sMax]))

# Show path samples sValues
fig, ax = plt.subplots(1,1)
ax.plot(sValues, '-*')
ax.grid(True)


# Compute all trailer positions from path derivatives at all sValues
def trailerPositions(s):
    SX = np.zeros((len(bb), len(s)))
    SY = np.zeros((len(bb), len(s)))
    x = np.zeros((len(bb)))
    x[1] = lx / sMax     # x 1st derivative
    y = np.zeros((len(bb)))        
    for k in range(len(s)):
        x[0] = lx * s[k] / sMax # x pos
        x[1] = lx / sMax     # x 1st derivative
        for l in range(len(bb)):
            y[l] = bb[l](s[k])
        sx, sy, vx, vy = tp.trailers_positions_r(x, y, L)
        SX[:,k] = sx
        SY[:,k] = sy
    return SX, SY

SX, SY = trailerPositions(sValues)


if False:       
    anim = animTrailers(SX, SY)
    aa = anim.anim()

if False:
    aa.save('anim.gif', writer='imagemagick', fps=25)
    
if True:
    fileName = "data/SXSY_n%d.npy" % n
    with open(fileName, 'wb') as f:
        np.save(f, SX)
        np.save(f, SY)
        f.close()