#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 17:58:58 2020

@author: basile
"""

# Binomial coefficients
# from https://gist.github.com/rougier/ebe734dcc6f4ff450abf
# Faster than scipy.special.binom
def binomial(n, k):
    """
    Binomial coefficient (n k)
    """
    if not 0 <= k <= n:
        return 0
    b = 1
    for t in range(min(k, n-k)):
        b *= n
        b //= t+1
        n -= 1
    return b

# Bell polynomial evaluation
# https://en.wikipedia.org/wiki/Bell_polynomials
def bell(n,k,x):
    """
    Evaluate the partial exponential Bell polynomial B_n,k(x)
    """
    if (n==0) & (k==0):
        return 1
    elif (k==0) | (n==0):
        return 0
    else:
        b = 0
        for i in range(n-k+1):
            b += binomial(n-1, i) * x[i] * bell(n-i-1, k-1, x)
        return b
    
# Get n-th derivative of composition f(g(x))
def composition_rule_nth(f,g):
    """    
    Compute the n-th derivative of f(g(x)) w.r.t. x given the
    list of derivatives of f at g(x) and of g at x using 
    Faa di Bruno's formula and Bell polynomials.
    Parameters:
        
        f : list of derivatives of f. f = [f^(1)(g(x)), ..., f^(n)(g(x))]
    
        g : list of derivatives of g. g = [g^(1)(x),    ..., g^(n)(x)]
    """
    assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
    n = len(f)
    dfg = 0
    for k in range(n):
        dfg += f[k] * bell(n, k+1, g[:n-k])
    return dfg


def composition_rule(f,g):
    """    
    Compute the derivatives of f(g(x)) w.r.t. x given the
    list of derivatives of f at g(x) and of g at x using 
    Faa di Bruno's formula and Bell polynomials.
    Parameters:
        
        f : list of derivatives of f. f = [f^(0)(g(x)), f^(1)(g(x)), ..., f^(n)(g(x))]
    
        g : list of derivatives of g. g = [g^(0)(x),    g^(1)(x),    ..., g^(n)(x)]
    compute the list
        h : list of derivatives of h. h = [h^(0)(x),    h^(1)(x),    ..., h^(n)(x)]
    where h(x) = f(g(x))
    """
    assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
    n = len(f)
    h = [0] * n
    h[0] = f[0]
    for k in range(1,n):
        h[k] = composition_rule_nth(f[1:k+1], g[1:k+1])
    return h