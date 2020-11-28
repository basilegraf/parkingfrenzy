#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:00:46 2020

@author: basile
"""

import numpy as np

# Derivaties of f(x) * h(x)
def product_rule(f,g):
    """
    Higher order product rule. Given the lists f and g of function derivatives
        f = [f(x), f^(1)(x), ... , f^(n)(x)]
        
        g = [g(x), g^(1)(x), ... , g^(n)(x)]
    compute the list
        h = [h(x), h^(1)(x), ... , h^(n)(x)]
    where h(x) = f(x) * g(x).
    """
    assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
    n = len(f)
    h = [0] * n
    ker = [1,1]
    coeffs = [1]
    for k in range(n):       
        v = np.multiply(f[:k+1], g[k::-1])
        h[k] = np.dot(coeffs, v)
        coeffs = np.convolve(ker, coeffs)
    return h


# Derivaties of 1/f(x)
def reciprocal_rule(f):
    """
    Higher order derivatives of 1/f(x)
        f = [f(x), f^(1)(x), ... , f^(n)(x)]
    compute the list
        h = [h(x), h^(1)(x), ... , h^(n)(x)]
    where h(x) = 1/f(x).
    """
    n = len(f)
    h = [0] * n
    ker = [1,1]
    coeffs = [1]
    h[0] = 1 / f[0]
    for k in range(1,n):  
        coeffs = np.convolve(ker, coeffs)        
        v = np.multiply(f[1:k+1], h[k-1::-1])
        w = np.dot(coeffs[1:], v);
        h[k] = - w / f [0]       
    return h

# Derivaties of f(x) / g(x)
def quotient_rule(f,g):
    """
    Higher order quatient rule. Given the lists f and g of function derivatives
        f = [f(x), f^(1)(x), ... , f^(n)(x)]
        
        g = [g(x), g^(1)(x), ... , g^(n)(x)]
    compute the list
        h = [h(x), h^(1)(x), ... , h^(n)(x)]
    where h(x) = f(x) / g(x).
    """
    assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
    rg = reciprocal_rule(g)
    return product_rule(f, rg)