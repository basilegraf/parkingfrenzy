#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 10:49:33 2020

@author: basile
"""

import numpy as np

# h(x) = f(x) * g(x) mod O(x^(n+1))
def power_series_prod(f, g):
    assert len(f) == len(g), "f and g must be of the same length"
    n = len(f) - 1
    h = [0] * (n + 1)
    for k in range(n + 1):
        for l in range(k + 1):
            h[k] += f[l] * g[k - l]
    return h
            
            
# h(x) = f(g(x)) mod O(x^(n+1))
def power_series_comp(f, g):
    assert len(f) == len(g), "f and g must be of the same length"
    n = len(f) - 1
    h = [0] * (n + 1)
    # degree zero of result h
    h[0] = f[0]
    # mono: monomial g(x)^k
    mono = [0] * (n + 1) 
    mono[0] = 1 # g(x)^0
    # compute degrees 1,...,n
    for k in range(1, n + 1):
        mono = power_series_prod(mono, g)
        for q in range(n + 1):
            h[q] += f[k] * mono[q]
    return h

def composition_rule(f, g):
    """    
    Compute the derivatives of f(g(x)) w.r.t. x given the
    list of derivatives of f at g(x) and of g at x using 
    truncated power series composition
    Parameters:
        
        f : list of derivatives of f. f = [f^(0)(g(x)), f^(1)(g(x)), ..., f^(n)(g(x))]
    
        g : list of derivatives of g. g = [g^(0)(x),    g^(1)(x),    ..., g^(n)(x)]
    compute the list
        h : list of derivatives of h. h = [h^(0)(x),    h^(1)(x),    ..., h^(n)(x)]
    where h(x) = f(g(x))
    """
    assert len(f) == len(g), "f and g must be of the same length"
    n = len(f) - 1
    # Constant power series case => value is f[0] independently of g
    if n == 0:
        return f
    # Non trivial cases
    p1 = f.copy()
    p2 = [0] * (n+1)
    p2[0] = -g[0]
    p2[1] = 1
    p3 = g.copy()
    kfac = 1
    for k in range(n + 1):
        p1[k] *= kfac 
        p3[k] *= kfac 
        kfac /= k + 1
    h = power_series_comp(p2, p3)
    h = power_series_comp(p1, h)
    kfac = 1
    for k in range(n + 1):
        h[k] *= kfac
        kfac *= k + 1
    return h
        
        

if __name__ == "__main__":
    import sympy as sp
    import time
           
    def spoly(c, x):
        p = 0
        for k in range(len(c)):
            p += c[k] * x**k
        return p
    
    # Coefficient lists examples         
    f = [1,2,4,2]
    g = [4,-2,5,-2]
    
    # Compute poser series directly with sympy
    x = sp.symbols('x')
    fs = spoly(f, x)
    gs = spoly(g, x)   
    fgs = sp.expand(fs.subs(x,gs))
    fg1 = list(map(lambda k : fgs.coeff(x,k), list(range(len(f))))) # truncate
    
    # Compute the same with our function
    fg2 = power_series_comp(f, g)
    
    print("power series composition sympy    : ", fg1)
    print("power series composition numerical: ", fg2)
    
    # timing
    n = 100
    fnum = 1e-10*np.random.randn(n)
    gnum = 1e-10*np.random.randn(n)
    
    t0 = time.time()
    fgnum = composition_rule(fnum, gnum)
    t1 = time.time()
    print("Time :", t1-t0)
    print("Composition: ", fgnum)
    