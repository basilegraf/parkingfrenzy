#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 14:33:02 2020

@author: basile
"""


import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
from matplotlib.collections import PatchCollection

width = 0.5
length = 0.8
angle = 30
chassis = plt.Rectangle([-width/2,0], width, length, angle)
wheell = plt.Rectangle([-width/2,0], width/10, length/4, angle)
wheelr = plt.Rectangle([width/2-width/10,0], width/10, length/4, angle)

patches = [chassis, wheell, wheelr]

collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3)

fig, ax = plt.subplots()
ax.axis('equal')
ax.set_xlim(-3,3)
ax.set_ylim(-3,3)
ax.grid(True)


#ax.add_collection(collection)


class trailer:
    def __init__(self, ax, width, length):
        self.ax = ax
        self.chassis_pos = np.array([-width/2, 0])
        self.rwheell_pos = np.array([-width/1.8, -length/16])
        self.rwheelr_pos = np.array([width/1.8-width/10, -length/16])
        
        self.fwheell_pos = np.array([-width/1.8, -length/8])
        self.fwheelr_pos = np.array([width/1.8-width/10, -length/8])
        
        self.chassis = plt.Rectangle(self.chassis_pos, width, length, angle=0, color='blue')
        self.rwheell = plt.Rectangle(self.rwheell_pos, width/10, length/3, angle=0, color='black')
        self.rwheelr = plt.Rectangle(self.rwheelr_pos, width/10, length/3, angle=0, color='black')
        ax.add_patch(self.chassis)
        ax.add_patch(self.rwheell)
        ax.add_patch(self.rwheelr)
    
    def move(self, pos, alpha):
        ca = np.cos(alpha)
        sa = np.sin(alpha)
        R = np.array([[ca, -sa],[sa, ca]])
        self.chassis.xy = pos + np.matmul(R, self.chassis_pos)
        self.rwheell.xy = pos + np.matmul(R, self.rwheell_pos)
        self.rwheelr.xy = pos + np.matmul(R, self.rwheelr_pos)
        self.chassis.angle = 180 * alpha / np.pi;
        self.rwheell.angle = 180 * alpha / np.pi;
        self.rwheelr.angle = 180 * alpha / np.pi;
        
        
        
t=trailer(ax, 0.5,0.8)       

t.move([1,0.5], 0.3)       
        
        
        
        
        