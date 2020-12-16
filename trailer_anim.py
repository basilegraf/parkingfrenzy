#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:52:26 2020

@author: basile
"""

import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl

# Use qt for animations
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass

# degree to load from result file
n = 5

# load data
fileName = "data/SXSY_n%d.npy" % n
with open(fileName, 'rb') as f:
    SX = np.load(f)
    SY = np.load(f)
    f.close()
    
# class for displaying a single trailer
class trailer_show:
    def __init__(self, ax, length, width):
        self.ax = ax
        self.width = width
        self.length = length
        self.xy = [0 ,0]
        angle = 0
        chassis = plt.Rectangle([-width/2,0], width, length, angle)
        weell = plt.Rectangle([-width/2,0], width/10, length/4, angle)
        weelr = plt.Rectangle([width/2-width/10,0], width/10, length/4, angle)
        ax.add_patch(chassis)
        ax.add_patch(weell)
        ax.add_patch(weelr)
        
    def show(xyIn,a):
        self.xy = np.asarray(xyIn)       
        c, s = np.cos(a), np.sin(a)
        R = np.array([[c, -s], [s, c]])
        
        self.chassis.xy = xy + np.matmul(R, [-width/2,0])
        
        
    


class animTrailers:
    def __init__(self, SX, SY):
        self.fig, self.ax = plt.subplots()
        self.SX = SX
        self.SY = SY
        self.frames = range(SX.shape[1])
        
    def initAnim(self):
        self.ax.clear()
        self.ax.plot(self.SX.transpose(), self.SY.transpose())
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
 
     
anim = animTrailers(SX, SY)
aa = anim.anim()