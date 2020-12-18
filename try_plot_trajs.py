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
import matplotlib.animation as animation
import matplotlib as mpl
from matplotlib.collections import PatchCollection




class animText:
    def __init__(self, n):
        self.fig, self.ax = plt.subplots()
        self.frames = range(75)
        self.fig.set_size_inches(19.20, 10.80, True)
        self.fig.set_dpi(100)
        self.fig.tight_layout()
        self.n = n
        
    def initAnim(self):
        self.ax.clear()
        self.ax.axis('off')

        txt=plt.text(  # position text relative to Figure
            0.5, 0.5, '$n=%d$' % self.n,
            ha='center', va='center',
            transform=self.fig.transFigure,
            fontsize=50, 
            color = 'xkcd:yellow orange',
            usetex=True)
        self.ax.add_artist(txt)
        self.ax.grid(b=False)
        
    def updateText(self, frame):
        1
    def anim(self):
        return FuncAnimation(self.fig, self.updateText, self.frames, init_func=self.initAnim, blit=False, repeat_delay=1000, interval=20)
 
     
n = 10
anim = animText(n)
aa = anim.anim()

if True:
    brate = 1500
    fileName = "data/Text_%d.mp4" % n
    writer = animation.FFMpegWriter(fps=25, metadata=dict(artist='Ugarte'), bitrate=brate)
    aa.save(fileName, writer=writer,dpi=100, savefig_kwargs=dict(facecolor=(0,0,0)))

