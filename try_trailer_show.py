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
ax.set_xlim(-3,6)
ax.set_ylim(-3,3)
ax.grid(True)


#ax.add_collection(collection)


class car:
    def __init__(self, ax, width, length):
        self.ax = ax
        wheel_wid = width / 7;
        wheel_len = length / 3;
        axle_wid = width / 20
        # vector from wheel center to wheel lower-left corner
        self.wheel_off = np.array([-wheel_wid/2, -wheel_len/2])
        
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
        self.link_pos = np.array([-axle_wid/2, 0])
        
        self.chassis = plt.Rectangle(self.chassis_pos, width, length, angle=0, color='xkcd:ocean blue')
        
        self.rwheell = plt.Rectangle(self.rwheell_pos, wheel_wid, wheel_len, angle=0, color='black')
        self.rwheelr = plt.Rectangle(self.rwheelr_pos, wheel_wid, wheel_len, angle=0, color='black')
        
        self.fwheell = plt.Rectangle(self.fwheell_cpos + self.wheel_off, wheel_wid, wheel_len, angle=0, color='black')
        self.fwheelr = plt.Rectangle(self.fwheelr_cpos + self.wheel_off, wheel_wid, wheel_len, angle=0, color='black')
        
        self.raxle = plt.Rectangle(self.raxle_pos, width, axle_wid, angle=0, color='black')
        self.faxle = plt.Rectangle(self.faxle_pos, width, axle_wid, angle=0, color='black')
        self.link = plt.Rectangle(self.link_pos, axle_wid, length, angle=0, color='black')
        
        ax.add_patch(self.chassis)
        ax.add_patch(self.rwheell)
        ax.add_patch(self.rwheelr)
        ax.add_patch(self.fwheell)
        ax.add_patch(self.fwheelr)
        ax.add_patch(self.raxle)
        ax.add_patch(self.faxle)
        ax.add_patch(self.link)
        
    
    def move(self, pos, angle1, angle2):
        alpha1 = angle1 - np.pi / 2
        alpha2 = angle2 - np.pi / 2
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
        self.link.xy = pos + np.matmul(R1, self.link_pos)
        self.chassis.angle = 180 * alpha1 / np.pi;
        self.rwheell.angle = 180 * alpha1 / np.pi;
        self.rwheelr.angle = 180 * alpha1 / np.pi;
        self.raxle.angle = 180 * alpha1 / np.pi;
        self.faxle.angle = 180 * alpha1 / np.pi;
        self.link.angle = 180 * alpha1 / np.pi;
        
        self.fwheell.xy = pos + np.matmul(R1, self.fwheell_cpos) + np.matmul(R2, self.wheel_off)
        self.fwheelr.xy = pos + np.matmul(R1, self.fwheelr_cpos) + np.matmul(R2, self.wheel_off)
        self.fwheell.angle = 180 * alpha2 / np.pi;
        self.fwheelr.angle = 180 * alpha2 / np.pi;
        
    def alpha(self, alpha):
        self.chassis.set_alpha(alpha)
        self.rwheell.set_alpha(alpha)
        self.rwheelr.set_alpha(alpha)
        self.fwheell.set_alpha(alpha)
        self.fwheelr.set_alpha(alpha)
        self.raxle.set_alpha(alpha)
        self.faxle.set_alpha(alpha)
        self.link.set_alpha(alpha)
        
        

class trailer:
    def __init__(self, ax, width, length):
        self.ax = ax
        wheel_wid = width / 7;
        wheel_len = length / 3;
        axle_wid = width / 20
        # vector from wheel center to wheel lower-left corner
        self.wheel_off = np.array([-wheel_wid/2, -wheel_len/2])
        
        # rear wheels are fixed relative to chassis (lower-left corner pos)
        self.chassis_pos = np.array([-width/2, 0])
        self.rwheell_pos = np.array([-width/2, 0]) + self.wheel_off
        self.rwheelr_pos = np.array([width/2, 0]) + self.wheel_off
        
        # axle
        self.raxle_pos = np.array([-width/2, -axle_wid/2])
        self.link_pos = np.array([-axle_wid/2, 0])
        
        self.chassis = plt.Rectangle(self.chassis_pos, width, length/2, angle=0, color='xkcd:ocean blue')
        
        self.rwheell = plt.Rectangle(self.rwheell_pos, wheel_wid, wheel_len, angle=0, color='black')
        self.rwheelr = plt.Rectangle(self.rwheelr_pos, wheel_wid, wheel_len, angle=0, color='black')

        self.raxle = plt.Rectangle(self.raxle_pos, width, axle_wid, angle=0, color='black')
        self.link = plt.Rectangle(self.link_pos, axle_wid, length, angle=0, color='black')
        
        ax.add_patch(self.chassis)
        ax.add_patch(self.rwheell)
        ax.add_patch(self.rwheelr)
        ax.add_patch(self.raxle)
        ax.add_patch(self.link)

        
    
    def move(self, pos, angle1):
        alpha1 = angle1 - np.pi / 2
        ca = np.cos(alpha1)
        sa = np.sin(alpha1)
        R1 = np.array([[ca, -sa],[sa, ca]])
        self.chassis.xy = pos + np.matmul(R1, self.chassis_pos)
        self.rwheell.xy = pos + np.matmul(R1, self.rwheell_pos)
        self.rwheelr.xy = pos + np.matmul(R1, self.rwheelr_pos)
        self.raxle.xy = pos + np.matmul(R1, self.raxle_pos)
        self.link.xy = pos + np.matmul(R1, self.link_pos)
        self.chassis.angle = 180 * alpha1 / np.pi;
        self.rwheell.angle = 180 * alpha1 / np.pi;
        self.rwheelr.angle = 180 * alpha1 / np.pi;
        self.raxle.angle = 180 * alpha1 / np.pi;
        self.link.angle = 180 * alpha1 / np.pi;
        
    def alpha(self, alpha):
        self.chassis.set_alpha(alpha)
        self.rwheell.set_alpha(alpha)
        self.rwheelr.set_alpha(alpha)
        self.raxle.set_alpha(alpha)
        self.link.set_alpha(alpha)
     
        
     
        
class train:
    def __init__(self, ax, width, lengths):
        assert len(lengths) >= 3
        self.vehicles = [];
        pos = 0
        # trailers
        for k in range(len(lengths) - 2):
            self.vehicles.append(trailer(ax, width, lengths[k]))
            self.vehicles[k].move([pos, 0], 0)
            pos += lengths[k]
        # head car (last lengths value actually not used)
        self.vehicles.append(car(ax,width,lengths[-2]))
        self.vehicles[-1].move([pos, 0], 0, 0)   
        
    def place(self, x, y):
        assert len(x) == len(y)
        assert len(x) == len(self.vehicles) + 2
        angles = list(map(np.arctan2, np.diff(y), np.diff(x)))
        print("angles = ", angles)
        for k in range(len(self.vehicles) - 1):           
            self.vehicles[k].move([x[k], y[k]], angles[k])
        self.vehicles[-1].move([x[-3], y[-3]], angles[-2], angles[-1])
    
    def alpha(self, alpha):
        for v in self.vehicles:
            v.alpha(alpha)
            
            
            
# c=car(ax, 0.5,0.8)    

# t = trailer(ax, 0.5, 0.8)   

# c.move([1,0.5], 0.3, 0.6)       
# t.move([-.4, 0.8], 0.4)      

# c.alpha(1)
# t.alpha(0.5)

            
# degree to load from result file
n = 5

# load data
fileName = "data/SXSY_n%d.npy" % n
with open(fileName, 'rb') as f:
    SX = np.load(f)
    SY = np.load(f)
    f.close()
    
Lengths = np.sqrt(np.diff(SX[:,0])**2 + np.diff(SY[:,0])**2)
Width = min(Lengths) / 2
        


tr = train(ax, 0.5, Lengths)
tr.alpha(0.5)   
tr.place(SX[:,200],SY[:,200])      
plt.plot(SX[:,200],SY[:,200])        