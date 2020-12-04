#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:54:45 2020

@author: basile
"""

import numpy as np
from cpython cimport array
import array

# Rescaled derivaties of f(x) * h(x)
# The result is symply the truncation at degree n of the convolution product 
# of the lists f and g
cdef void product_rule_rc(double[:] f,double[:] g, double[:] h, int n):
    """
    Higher order product rule. Given the lists f and g of function derivatives
        f = [f(x), f^[1](x), ... , f^[n](x)]
        
        g = [g(x), g^[1](x), ... , g^[n](x)]
    compute the list
        h = [h(x), h^[1](x), ... , h^[n](x)]
        
    where h(x) = f(x) * g(x) and a^[k] means
    
        a^[k](x) := (1/factorial(k)) * a^(k)(x)
    """
    cdef int k, l
    for k in range(n):     
        h[k] = 0.0
        for l in range(k+1):
            h[k] += f[l] * g[k-l]
            
# Wrapper for product_rule_rc (use for test only)
# https://docs.cython.org/en/latest/src/tutorial/array.html
# https://docs.python.org/3/library/array.html
def product_rule_r(ff, gg):
    assert len(ff) == len(gg), "Arrays should have same length"
    cdef array.array f = array.array('d', ff)
    cdef double[:] cf = f
    cdef array.array g = array.array('d', gg)
    cdef double[:] cg = g
    cdef array.array h = array.array('d', [0] * len(f))
    cdef double[:] ch = h
    cdef int n = len(f)
    product_rule_rc(cf, cg, ch, n)
    return np.array(h)


# Derivaties of 1/f(x)
cdef void reciprocal_rule_rc(double[:] f, double[:] h, int n):
    """
    Higher order derivatives of 1/f(x)
        f = [f(x), f^[1](x), ... , f^[n](x)]
    compute the list
        h = [h(x), h^[1](x), ... , h^[n](x)]
    where h(x) = 1/f(x) and a^[k] means
    
        a^[k](x) := (1/factorial(k)) * a^(k)(x)
    """
    cdef int k, l
    h[0] = 1 / f[0]
    for k in range(1,n):  
        w = 0
        for l in range(1,k+1):
            w += f[l] * h[k-l]
        h[k] = - w / f [0]       
        
# Wrapper for reciprocal_rule_rc (use for test only)
# https://docs.cython.org/en/latest/src/tutorial/array.html
# https://docs.python.org/3/library/array.html
def reciprocal_rule_r(ff):
    cdef array.array f = array.array('d', ff)
    cdef double[:] cf = f
    cdef array.array h = array.array('d', [0] * len(f))
    cdef double[:] ch = h
    cdef int n = len(f)
    reciprocal_rule_rc(cf, ch, n)
    return np.array(h)



# Derivaties of f(x) / g(x)
cdef void quotient_rule_rc(double[:] f,double[:] g, double[:] h, double[:] tmp, int n):
    """
    Higher order quotient rule. Given the lists f and g of function derivatives
        f = [f(x), f^[1](x), ... , f^[n](x)]
        
        g = [g(x), g^[1](x), ... , g^[n](x)]
    compute the list
        h = [h(x), h^[1](x), ... , h^[n](x)]
        
    where h(x) = f(x) * g(x) and a^[k] means
    
        a^[k](x) := (1/factorial(k)) * a^(k)(x)
    """
    reciprocal_rule_rc(g, tmp, n)
    product_rule_rc(f, tmp, h, n)


# Wrapper for product_rule_rc (use for test only)
# https://docs.cython.org/en/latest/src/tutorial/array.html
# https://docs.python.org/3/library/array.html
def quotient_rule_r(ff, gg):
    assert len(ff) == len(gg), "Arrays should have same length"
    cdef array.array f = array.array('d', ff)
    cdef double[:] cf = f
    cdef array.array g = array.array('d', gg)
    cdef double[:] cg = g
    cdef array.array h = array.array('d', [0] * len(f))
    cdef double[:] ch = h
    cdef array.array tmp = array.array('d', [0] * len(f))
    cdef double[:] ctmp = tmp
    cdef int n = len(f)
    quotient_rule_rc(cf, cg, ch, ctmp, n)
    return np.array(h)


# # h(x) = f(g(x)) mod O(x^(n+1))
# def poly_composition_rule_rc(f, g):
#     assert len(f) == len(g), "f and g must be of the same length"
#     n = len(f) - 1
#     h = [0] * (n + 1)
#     # degree zero of result h
#     h[0] = f[0]
#     # mono: monomial g(x)^k
#     mono = [0] * (n + 1) 
#     mono[0] = 1 # g(x)^0
#     # compute degrees 1,...,n
#     for k in range(1, n + 1):
#         mono = product_rule_r(mono, g)
#         for q in range(n + 1):
#             h[q] += f[k] * mono[q]
#     return h


# def composition_rule_rc(f, g):
#     """    
#     Compute the derivatives of f(g(x)) w.r.t. x given the
#     list of derivatives of f at g(x) and of g at x using 
#     truncated power series composition
#     Parameters:
        
#         f : list of derivatives of f. f = [f^[0](g(x)), f^[1](g(x)), ..., f^[1](g(x))]
    
#         g : list of derivatives of g. g = [g^[0](x),    g^[1](x),    ..., g^[1](x)]
#     compute the list
#         h : list of derivatives of h. h = [h^[0](x),    h^[1]x),    ..., h^[1](x)]
#     where h(x) = f(g(x))
#     """
#     assert len(f) == len(g), "f and g must be of the same length"
#     n = len(f) - 1
#     # Constant power series case => value is f[0] independently of g
#     if n == 0:
#         return f
#     # Non trivial cases
#     p1 = f.copy()
#     p2 = [0] * (n+1)
#     p2[0] = -g[0]
#     p2[1] = 1
#     p3 = g.copy()
#     h = poly_composition_rule_r(p2, p3)
#     h = poly_composition_rule_r(p1, h)
#     return h