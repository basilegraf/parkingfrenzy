#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:50:47 2020

In the equations, k is an index, not the independent variable

(x[k+1])    (x'[k])               L[k]             (x'[k])
(      )  = (     )  +  ----------------------- *  (     )
(y[k+1])    (y'[k])     sqrt(x'[k]^2 + y'[k]^2)    (y'[k])


            (x'[k])              (cos(a[k]))
          = (     )  +  L[k]  *  (         ) 
            (y'[k])              (sin(a[k]))
             
with

a[k] = arctan(y'[k], x'[k])
      
        x'[k] * y''[k] - y'[k] * x''[k]
a'[k] = -------------------------------
              x'[k]^2 + y'[k]^2
              
              
The higher order derivatives a'', a''', etc can then be obtained by applying 
product and quotient rules             
@author: basile
"""

import numpy as np
import sympy as sp

import product_quotient_rules as proquo
import faa_di_bruno as bruno
import truncated_power_series as trunc



def angle_derivatives(xIn, yIn):
    x = np.asarray(xIn)
    y = np.asarray(yIn)
    assert len(x) == len(y), "f and g must be of the same length"
    assert len(x) >= 2, "x and y must each contain at least 1 element"
    # value of a (no derivatives)
    a0 = np.asarray([np.arctan2(y[1], x[1])])
    if len(x) > 2:
        # derivatives of x'*y''
        xdydd = np.asarray(proquo.product_rule(x[1:-1], y[2:]))
        # derivatives of x''*y'
        xddyd = np.asarray(proquo.product_rule(x[2:], y[1:-1]))
        # derivative of x'**2
        xdxd = np.asarray(proquo.product_rule(x[1:-1], x[1:-1]))
        # derivative of y'**2
        ydyd = np.asarray(proquo.product_rule(y[1:-1], y[1:-1]))
        # derivatives of a'
        ad = np.asarray(proquo.quotient_rule(xdydd - xddyd, xdxd + ydyd))
        # derivatives of a including a0
        a = np.concatenate((a0, ad))
    else:
        a = a0
    return a
    

def cosine_sine_derivatives(aIn):
    a = np.asarray(aIn)
    # derivatives of [cos(y), sin(y)]
    cs = np.zeros((2,len(a)))
    cs[0,0] = np.cos(a[0])
    cs[1,0] = np.sin(a[0])
    d = np.array([[0,-1],[1,0]])
    for k in range(len(a) - 1):
        cs[:,k+1] = np.matmul(d, cs[:,k])
    # derivatives of cos(a(x))
    c = np.asarray(trunc.composition_rule(cs[0,:], a))
    # derivatives of sin(a(x))
    s = np.asarray(trunc.composition_rule(cs[1,:], a))
    return c, s
        
# Derivatives of x[k+1] y[k+1] from derivatives of x[k],y[k] and length L[k]
def front_trailer_derivatives(xkIn, ykIn, Lk):
    xk = np.asarray(xkIn)
    yk = np.asarray(ykIn)
    a = angle_derivatives(xk, yk)
    c, s = cosine_sine_derivatives(a)
    xk1 = xk[:-1] + Lk * c
    yk1 = yk[:-1] + Lk * s
    return xk1, yk1

def trailers_positions(x0In, y0In, Lin):
    assert len(x0In) == len(y0In), "x0 and y0 must be of the same length"
    assert len(Lin) + 1 == len(x0In), "L must have length len(x0) - 1"
    x = np.asarray(x0In).copy()
    y = np.asarray(y0In).copy()
    L = np.asarray(Lin)
    xk = np.zeros(len(x))
    yk = np.zeros(len(y))
    xdk = np.zeros(len(x) - 1)
    ydk = np.zeros(len(y) - 1)   
    xk[0] = x[0]
    yk[0] = y[0]
    xdk[0] = x[0]
    ydk[0] = y[0]
    for k in range(1, len(x)):
        x,y = front_trailer_derivatives(x.copy(), y.copy(), L[k-1])
        xk[k] = x[0]
        yk[k] = y[0]
        if len(x) > 1:
            xdk[k] = x[1]
            ydk[k] = y[1]
    return xk, yk, xdk, ydk
        
            
        
        
    
    

