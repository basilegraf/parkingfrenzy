#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 10:33:49 2020

@author: basile
"""

import sympy as sp
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt
import scipy.interpolate as interp
from matplotlib.animation import FuncAnimation

# Use qt for animations
try:
    import IPython
    shell = IPython.get_ipython()
    shell.enable_matplotlib(gui='qt')
except:
    pass


N = 4

# Car k, x coordinate
x = sp.symbols('xk:%d'%N)           # derivatives 0 to N-1
xd = sp.symbols('xk(1:%d)'%(N+1))   # derivatives 1 to N
xxd = sp.symbols('xk:%d'%(N+1))     # derivatives 0 to N

# yCar k,  coordinate
y = sp.symbols('yk:%d'%N)
yd = sp.symbols('yk(1:%d)'%(N+1))
yyd = sp.symbols('yk:%d'%(N+1))

# Car k, length
Lk = sp.symbols('Lk')

xyk1 = sp.Matrix([x[0]+(Lk*x[1])/sp.sqrt(x[1]**2+y[1]**2), y[0]+(Lk*y[1])/sp.sqrt(x[1]**2+y[1]**2)])

# One derivative stage
def stage(xyk):
    return xyk.jacobian(x) * sp.Matrix(xd) + xyk.jacobian(y) * sp.Matrix(yd)

# List of all derivatives
XY=[xyk1]
for k in range(1,N):
    XY.append(stage(XY[-1]))
    
# Build functions for evaluation
fun=[]
for k in range(N):
    fun.append(sp.lambdify(((xxd),(yyd),(Lk),),XY[k]))
    
# Compute x0,..,xN-1 and y0,...,yN-1 from x and y
def mapping(x,y,LL,N):
    xk=x
    yk=y
    X=[x[0]]
    Y=[y[0]]
    for k in range(N):      
        xk1=np.zeros((N+1))
        yk1=np.zeros((N+1))
        for q in range(N-k):
            xyk1q=fun[q](xk,yk,LL[k]);
            xk1[q]=xyk1q[0]
            yk1[q]=xyk1q[1]
        X.append(xk1[0])
        Y.append(yk1[0])
        xk=xk1
        yk=yk1
    return X,Y
        
# BSpline trajectory for x[0], y[0]
M=N+2 # Spline degree to use

# Sigmoid function
t=np.concatenate((np.zeros((M)), np.linspace(0,2,2*M+1)))
cy=np.concatenate((np.zeros((M)), np.ones((1*M))))
by = interp.BSpline(t,cy,M)
tEval = np.linspace(0,1,100)

fac = 1;
for k in range(N+1):
    fac *= k+1
    plt.plot(tEval,by.derivative(k)(tEval)/fac**2)
    
# Linear function
cx=np.ones(3*M+1)
bx = interp.BSpline(t,cx,M)
bx = bx.antiderivative(1)

plt.figure
for k in range(N+1):
    plt.plot(tEval,bx.derivative(k)(tEval))

    
