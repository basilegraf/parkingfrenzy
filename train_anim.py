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
import matplotlib.animation as animation
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

# fig, ax = plt.subplots()
# ax.axis('equal')
# ax.set_xlim(-3,6)
# ax.set_ylim(-3,3)
# ax.grid(True)


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
n = 10

# load data
fileName = "data/SXSY_n%d.npy" % n
with open(fileName, 'rb') as f:
    SX = np.load(f)
    SY = np.load(f)
    f.close()
    
Lengths = np.sqrt(np.diff(SX[:,0])**2 + np.diff(SY[:,0])**2)
Width = min(Lengths) / 2
        


# tr = train(ax, Width, Lengths)
# tr.alpha(0.5)   
# tr.place(SX[:,200],SY[:,200])      
# plt.plot(SX[:,200],SY[:,200])       


class background:
    def __init__(self, SX, SY, ax):
        n = len(SX[:,0])
        marg = (np.max(SX) - np.min(SX))/200  
        
        xrange = np.array([np.min(SX)-marg, np.max(SX)+marg])
        yrange = np.array([np.min(SY), np.max(SY)])
        ydisp = abs(np.max(SY[0,:])-np.min(SY[0,:]))
        lanewidth = 1.2*ydisp
        parkingwidth = 0.8*ydisp
        trainlength = abs(np.max(SX[:,0])-np.min(SX[:,0]))
        trailerLength = trainlength / n
        
        self.patches = []
        self.patches.append(plt.Rectangle([np.min(SX)-marg, np.min(SY)-marg], np.max(SX)-np.min(SX)+2*marg, np.max(SY)-np.min(SY)+2*marg, color = 'xkcd:grass green'))
        self.patches.append(plt.Rectangle([np.min(SX)-marg,0.5*parkingwidth], np.max(SX)-np.min(SX)+2*marg, 2*lanewidth, color = 'gray'))
        parkxy = [-trailerLength/2,-0.5*parkingwidth]
        parklx = trainlength
        parkly= parkingwidth
        self.patches.append(plt.Rectangle(parkxy, parklx, parkly, color = 'gray'))
        
        
        lw = 4
        self.lines = []
        self.lines.append(mpl.lines.Line2D(xrange, 0*yrange+0.5*parkingwidth + lanewidth, color='white',linestyle='dashed', linewidth = lw))
        self.lines.append(mpl.lines.Line2D(xrange, 0*yrange+0.5*parkingwidth, color='white', linewidth = lw))
        self.lines.append(mpl.lines.Line2D(xrange, 0*yrange+0.5*parkingwidth + 2*lanewidth, color='white', linewidth = lw))
        # park lines
        self.lines.append(mpl.lines.Line2D([parkxy[0],parkxy[0]+parklx], [-0.5*parkingwidth,-0.5*parkingwidth], color='white', linewidth = lw))
        self.lines.append(mpl.lines.Line2D([parkxy[0],parkxy[0]], [-0.5*parkingwidth,0.5*parkingwidth], color='white', linewidth = lw))
        self.lines.append(mpl.lines.Line2D([parkxy[0]+parklx,parkxy[0]+parklx], [-0.5*parkingwidth,0.5*parkingwidth], color='white', linewidth = lw))
    
        for p in self.patches:
            ax.add_patch(p)
        for l in self.lines:
            ax.add_artist(l)
            
    def alpha(self, alpha):
        for p in self.patches:
            p.set_alpha(alpha)
        for l in self.lines:
            l.set_alpha(alpha)
    
    def zorder(self, zo):
        for p in self.patches:
            p.set_zorder(zo)
        for l in self.lines:
            l.set_zorder(zo)



class animTrain:
    def __init__(self, SX, SY):
        self.fig, self.ax = plt.subplots()
        self.SX = SX
        self.SY = SY
        self.frames = range(SX.shape[1])
        self.fig.set_size_inches(19.20, 10.80, True)
        self.fig.set_dpi(100)
        self.fig.tight_layout()
        
        
    def initAnim(self):
        self.ax.clear()
        self.ax.axis('off')
        self.ax.plot(self.SX[-1::-1,:].transpose(), self.SY[-1::-1,:].transpose(), zorder=-1000, alpha = 0.7)
        
        Lengths = np.sqrt(np.diff(SX[:,0])**2 + np.diff(SY[:,0])**2)
        Width = min(Lengths) / 2
        
        self.Back = background(self.SX, self.SY, self.ax)
        self.Back.alpha(1.0)
        self.Back.zorder(-500)
        
        self.Train = train(self.ax, Width, Lengths)
        self.Train.alpha(1.0) 
        
        self.Train.place(self.SX[:,0], self.SY[:,0]) 
        
        
        marg = (np.max(self.SX) - np.min(self.SX))/200   
        self.ln, = self.ax.plot(self.SX[:,0], self.SY[:,0], 'o-',linewidth=3, color='xkcd:scarlet', zorder=-5)
        self.ax.set_aspect(aspect='equal', adjustable='box')
        self.ax.set_xlim(left=np.min(self.SX)-marg, right=np.max(self.SX)+marg)
        self.ax.set_ylim(bottom=np.min(self.SY)-marg, top=np.max(self.SY)+marg)
        #self.ax.set_xbound(lower=-5, upper=5)
        #self.ax.set_ybound(lower=-0.5, upper=8)
        self.ax.grid(b=False)
        
    def updateTrain(self, frame):
        self.ln.set_xdata(self.SX[:, frame])
        self.ln.set_ydata(self.SY[:, frame])
        self.Train.place(self.SX[:, frame], self.SY[:, frame])  
        #self.ln, = self.ax.plot(self.TX[:,frame], self.TY[:,frame])
        alphaBegin = min(1.0, max(0.0, 2.0 - frame/100))
        n = len(self.SX[0, :])
        alphaEnd = min(1.0, max(0.0, 2.0 - (n-frame)/100))
        alpha = max(alphaBegin, alphaEnd)
        
        self.Back.alpha(alpha)
        self.Train.alpha(alpha)
       
    def anim(self):
        return FuncAnimation(self.fig, self.updateTrain, self.frames, init_func=self.initAnim, blit=False, repeat_delay=1000, interval=20)
 
     
if __name__ == "__main__":
    anim = animTrain(SX[:,::-1], SY[:,::-1])
    aa = anim.anim()
    aa.repeat = False
    if True:
        brate = 1500
        fileName = "data/Parking_%d_%d.mp4" % (n, brate)
        writer = animation.FFMpegWriter(fps=25, metadata=dict(artist='Ugarte'), bitrate=brate)
        aa.save(fileName, writer=writer,dpi=100, savefig_kwargs=dict(facecolor=(0,0,0)))