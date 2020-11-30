#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:10:59 2020

@author: basile
"""

import numpy as np

# Rescaled derivaties of f(x) * h(x)
# The result is symply the truncation at degree n of the convolution product 
# of the lists f and g
def product_rule_r(f,g):
    """
    Higher order product rule. Given the lists f and g of function derivatives
        f = [f(x), f^[1](x), ... , f^[n](x)]
        
        g = [g(x), g^[1](x), ... , g^[n](x)]
    compute the list
        h = [h(x), h^[1](x), ... , h^[n](x)]
        
    where h(x) = f(x) * g(x) and a^[k] means
    
        a^[k](x) := (1/factorial(k)) * a^(k)(x)
    """
    assert (len(f) == len(g)), "Lists of rescaled derivatives of f and g must be of the same length"
    n = len(f)
    h = [0] * n
    for k in range(n):       
        h[k] = np.dot(f[:k+1], g[k::-1])
    return h


# Derivaties of 1/f(x)
def reciprocal_rule_r(f):
    """
    Higher order derivatives of 1/f(x)
        f = [f(x), f^[1](x), ... , f^[n](x)]
    compute the list
        h = [h(x), h^[1](x), ... , h^[n](x)]
    where h(x) = 1/f(x) and a^[k] means
    
        a^[k](x) := (1/factorial(k)) * a^(k)(x)
    """
    n = len(f)
    h = [0] * n
    ker = [1,1]
    coeffs = [1]
    h[0] = 1 / f[0]
    for k in range(1,n):  
        coeffs = np.convolve(ker, coeffs)        
        w = np.dot(f[1:k+1], h[k-1::-1])
        h[k] = - w / f [0]       
    return h

# Derivaties of f(x) / g(x)
def quotient_rule_r(f,g):
    """
    Higher order quotient rule. Given the lists f and g of function derivatives
        f = [f(x), f^[1](x), ... , f^[n](x)]
        
        g = [g(x), g^[1](x), ... , g^[n](x)]
    compute the list
        h = [h(x), h^[1](x), ... , h^[n](x)]
        
    where h(x) = f(x) * g(x) and a^[k] means
    
        a^[k](x) := (1/factorial(k)) * a^(k)(x)
    """
    assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
    rg = reciprocal_rule_r(g)
    return product_rule_r(f, rg)