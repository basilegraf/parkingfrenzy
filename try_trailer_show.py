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


class car:
    def __init__(self, ax, width, length):
        self.ax = ax
        self.wid = width
        self.len = length
        self.wheel_wid = width / 10;
        self.wheel_len = length / 3;
        axle_wid = width / 20
        # vector from wheel center to wheel lower-left corner
        self.wheel_off = np.array([-self.wheel_wid/2, -self.wheel_len/2])
        
        # rear wheels are fixed relative to chassis (lower-left corner pos)
        self.chassis_pos = np.array([-width/2, 0])
        self.rwheell_pos = np.array([-width/2, 0]) + self.wheel_off
        self.rwheelr_pos = np.array([width/2, 0]) + self.wheel_off
        
        # front wheel centers
        self.fwheell_cpos = np.array([-width/2, length])
        self.fwheelr_cpos = np.array([width/2, length])
        
        # axles
        self.raxle_pos = np.array([-width/2, -axle_wid/2])
        self.faxle_pos = np.array([-width/2, length - axle_wid/2])
        
        self.chassis = plt.Rectangle(self.chassis_pos, width, length, angle=0, color='blue')
        
        self.rwheell = plt.Rectangle(self.rwheell_pos, self.wheel_wid, self.wheel_len, angle=0, color='black')
        self.rwheelr = plt.Rectangle(self.rwheelr_pos, self.wheel_wid, self.wheel_len, angle=0, color='black')
        
        self.fwheell = plt.Rectangle(self.fwheell_cpos + self.wheel_off, self.wheel_wid, self.wheel_len, angle=0, color='black')
        self.fwheelr = plt.Rectangle(self.fwheelr_cpos + self.wheel_off, self.wheel_wid, self.wheel_len, angle=0, color='black')
        
        self.raxle = plt.Rectangle(self.raxle_pos, width, axle_wid, angle=0, color='black')
        self.faxle = plt.Rectangle(self.faxle_pos, width, axle_wid, angle=0, color='black')
        
        ax.add_patch(self.chassis)
        ax.add_patch(self.rwheell)
        ax.add_patch(self.rwheelr)
        ax.add_patch(self.fwheell)
        ax.add_patch(self.fwheelr)
        ax.add_patch(self.raxle)
        ax.add_patch(self.faxle)
        
    
    def move(self, pos, alpha1, alpha2):
        ca = np.cos(alpha1)
        sa = np.sin(alpha1)
        R1 = np.array([[ca, -sa],[sa, ca]])
        ca = np.cos(alpha2)
        sa = np.sin(alpha2)
        R2 = np.array([[ca, -sa],[sa, ca]])
        self.chassis.xy = pos + np.matmul(R1, self.chassis_pos)
        self.rwheell.xy = pos + np.matmul(R1, self.rwheell_pos)
        self.rwheelr.xy = pos + np.matmul(R1, self.rwheelr_pos)
        self.raxle.xy = pos + np.matmul(R1, self.raxle_pos)
        self.faxle.xy = pos + np.matmul(R1, self.faxle_pos)
        self.chassis.angle = 180 * alpha1 / np.pi;
        self.rwheell.angle = 180 * alpha1 / np.pi;
        self.rwheelr.angle = 180 * alpha1 / np.pi;
        self.raxle.angle = 180 * alpha1 / np.pi;
        self.faxle.angle = 180 * alpha1 / np.pi;
        
        self.fwheell.xy = pos + np.matmul(R1, self.fwheell_cpos) + np.matmul(R2, self.wheel_off)
        self.fwheelr.xy = pos + np.matmul(R1, self.fwheelr_cpos) + np.matmul(R2, self.wheel_off)
        self.fwheell.angle = 180 * alpha2 / np.pi;
        self.fwheelr.angle = 180 * alpha2 / np.pi;
        

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
        
        
        
t=car(ax, 0.5,0.8)       

t.move([1,0.5], 0.3, 0.6)       
        
        
        
        
        