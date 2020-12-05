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

#import pyximport; pyximport.install()
import polynomial_rules_c as polyc
import product_quotient_rules_rescaled as poly
import math


def derivatives_to_poly(xIn):
    x = np.asarray(xIn, dtype='double')
    y = x.copy()
    fac = 1
    for k in range(len(x)):
        y[k] = x[k] / fac
        fac *= k + 1
    return y
        
def poly_to_derivatives(xIn):
    x = np.asarray(xIn, dtype='double')
    y = x.copy()
    fac = 1
    for k in range(len(x)):
        y[k] = x[k] * fac
        fac *= k + 1
    return y
    
    

# Takes a rescaled derivatives starting at degree d and rescale it such that it 
# becomes a list starting at degree 0
# The rescaling factor at k is
#    factorial(d+k)/factorial(k) = prod_{l=1,..,d} (k+l) 
def poly_shift(x, d):
    fac = np.ones(len(x))
    kList = np.array(range(len(x)))
    #kList[0] = 1
    for l in range(1,d+1):
        fac *= kList + l
    return fac * x
    


def angle_derivatives_r(xIn, yIn):
    x = np.asarray(xIn)
    y = np.asarray(yIn)
    assert len(x) == len(y), "f and g must be of the same length"
    assert len(x) >= 2, "x and y must each contain at least 1 element"
    # value of a (no derivatives)
    a0 = np.asarray([np.arctan2(y[1], x[1])])
    if len(x) > 2:
        # derivatives of x'*y''
        xdydd = polyc.product_rule_r(
            poly_shift(x[1:-1], 1), 
            poly_shift(y[2:], 2))
        # derivatives of x''*y'
        xddyd = polyc.product_rule_r(
            poly_shift(x[2:], 2), 
            poly_shift(y[1:-1], 1))
        # derivative of x'**2
        xdxd = polyc.product_rule_r(
            poly_shift(x[1:-1], 1), 
            poly_shift(x[1:-1], 1))
        # derivative of y'**2
        ydyd = polyc.product_rule_r(
            poly_shift(y[1:-1], 1), 
            poly_shift(y[1:-1], 1))
        # derivatives of a'
        ad = polyc.quotient_rule_r(
            xdydd - xddyd, 
            xdxd + ydyd)
        ad /= poly_shift(np.ones(len(ad)), 1)
        # derivatives of a including a0
        a = np.concatenate((a0, ad))
    else:
        a = a0
    return a
    

def cosine_sine_derivatives_r(aIn):
    a = np.asarray(aIn)
    # derivatives of [cos(y), sin(y)]
    cs = np.zeros((2,len(a)))
    cs[0,0] = np.cos(a[0])
    cs[1,0] = np.sin(a[0])
    d = np.array([[0,-1],[1,0]])
    for k in range(len(a) - 1):
        cs[:,k+1] = np.matmul(d, cs[:,k] / (k+1))
    # derivatives of cos(a(x))
    c = polyc.composition_rule_r(cs[0,:], a)
    # derivatives of sin(a(x))
    s = polyc.composition_rule_r(cs[1,:], a)
    return c, s
        
# Derivatives of x[k+1] y[k+1] from derivatives of x[k],y[k] and length L[k]
def front_trailer_derivatives_r(xkIn, ykIn, Lk):
    xk = np.asarray(xkIn)
    yk = np.asarray(ykIn)
    a = angle_derivatives_r(xk, yk)
    c, s = cosine_sine_derivatives_r(a)
    xk1 = xk[:-1] + Lk * c
    yk1 = yk[:-1] + Lk * s
    return xk1, yk1
    

if __name__ == "__main__":

    import trailer_derivatives as td
    n = 5
    x = np.random.rand(5)
    y = np.random.rand(5)
    Lk = 0.3
    
    xr = derivatives_to_poly(x)
    yr = derivatives_to_poly(y)
    
    
    x1r, y1r = front_trailer_derivatives_r(xr, yr, Lk)
    print(poly_to_derivatives(x1r), poly_to_derivatives(y1r))
    
    x1b, x2b = td.front_trailer_derivatives(x, y, Lk)
    print(x1b,x2b)
    
