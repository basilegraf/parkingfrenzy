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
    fnum = np.random.randn(n)
    gnum = np.random.randn(n)
    
    t0 = time.time()
    fgnum = power_series_comp(fnum, gnum)
    t1 = time.time()
    print("Time :", t1-t0)
    print("Composition: ", fgnum)
    