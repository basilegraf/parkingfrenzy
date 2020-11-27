#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:49:59 2020

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
            

def addd(a,b):
    return a+b


# Binomial coefficients
# from https://gist.github.com/rougier/ebe734dcc6f4ff450abf
# Faster than scipy.special.binom
cdef binomial(int n, int k):
    """
    Binomial coefficient (n k)
    """
    cdef int b, t
    if not 0 <= k <= n:
        return 0
    b = 1
    for t in range(min(k, n-k)):
        b *= n
        b /= t+1
        n -= 1
    return b

# Bell polynomial evaluation
# https://en.wikipedia.org/wiki/Bell_polynomials
cdef bell(int n, int k, x):
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
    
# # Get n-th derivative of composition f(g(x))
# def composition_rule_nth(f,g):
#     """    
#     Compute the n-th derivative of f(g(x)) w.r.t. x given the
#     list of derivatives of f at g(x) and of g at x using 
#     Faa di Bruno's formula and Bell polynomials.
#     Parameters:
        
#         f : list of derivatives of f. f = [f^(1)(g(x)), ..., f^(n)(g(x))]
    
#         g : list of derivatives of g. g = [g^(1)(x),    ..., g^(n)(x)]
#     """
#     assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
#     n = len(f)
#     dfg = 0
#     for k in range(n):
#         dfg += f[k] * bell(n, k+1, g[:n-k])
#     return dfg


# def composition_rule(f,g):
#     """    
#     Compute the derivatives of f(g(x)) w.r.t. x given the
#     list of derivatives of f at g(x) and of g at x using 
#     Faa di Bruno's formula and Bell polynomials.
#     Parameters:
        
#         f : list of derivatives of f. f = [f^(0)(g(x)), f^(1)(g(x)), ..., f^(n)(g(x))]
    
#         g : list of derivatives of g. g = [g^(0)(x),    g^(1)(x),    ..., g^(n)(x)]
#     compute the list
#         h : list of derivatives of h. h = [h^(0)(x),    h^(1)(x),    ..., h^(n)(x)]
#     where h(x) = f(g(x))
#     """
#     assert (len(f) == len(g)), "Lists of derivatives of f and g must be of the same length"
#     n = len(f)
#     h = [0] * n
#     h[0] = f[0]
#     for k in range(1,n):
#         h[k] = composition_rule_nth(f[1:k+1], g[1:k+1])
#     return h
    

if __name__ == "__main__":
    print('hello')
#     import sympy as sp
    
#     def nest_list(f,x,n):
#         fx = [0] * (n+1)
#         fx[0] = x
#         for k in range(n):
#             fx[k+1] = f(fx[k])
#         return fx
    
#     def derivatives_list(s,x,n):
#         f = lambda expr : sp.diff(expr, x)
#         return nest_list(f,s,n)
    
#     n = 4
#     x = sp.symbols('x')
#     # derivatives of f(x) w.r.t x
#     f = derivatives_list(sp.atan(x), x, n)    
#     # derivatives of g(x) w.r.t. x
#     g = derivatives_list(sp.ln(x), x, n)
    
#     # Product rule check
#     # Compute product derivatives with sympy directly
#     fg1 = derivatives_list(f[0] * g[0], x, n)
#     # Compute prodeuct derivatives using product_rule()
#     fg2 = product_rule(f,g)
#     check_fg = list(map(lambda s1,s2 : sp.simplify(s1-s2), fg1, fg2))
#     print('Product rule check: ', check_fg)
    
#     # Reciprocal rule check
#     # Compute reciprocal derivatives with sympy directly
#     rf1 = derivatives_list(1/f[0], x, n)
#     # Compute product derivatives using product_rule()
#     rf2 = reciprocal_rule(f)
#     check_rf = list(map(lambda s1,s2 : sp.simplify(s1-s2), rf1, rf2))
#     print('Reciprocal rule check: ', check_rf)
    
#     # Quotient rule check
#     # Compute quotient derivatives with sympy directly
#     qfg1 = derivatives_list(f[0] / g[0], x, n)
#     # Compute quotient derivatives using quotient_rule()
#     qfg2 = quotient_rule(f,g)
#     check_qfg = list(map(lambda s1,s2 : sp.simplify(s1-s2), qfg1, qfg2))
#     print('Quotient rule check: ', check_qfg)
    
    
#     # Composite derivatives check
#     # derivatives of f(x) w.r.t. x evaluated at x=g(x)
#     f_at_g = list(map(lambda y : y.subs(x,g[0]), f))
#     # devivatives of f(g(x)) w.r.t to x using sympy direcly
#     f_of_g1 = derivatives_list(f_at_g[0], x, n)
#     # n-th devivative of f(g(x)) w.r.t to x using Faa di Bruno
#     f_of_g2_n = composition_rule_nth(f_at_g[1:], g[1:])
#     # all devivatives of f(g(x)) w.r.t to x using Faa di Bruno
#     f_of_g2 = composition_rule(f_at_g, g)
#     print('n-th composite derivative check: ', sp.simplify(f_of_g1[-1]-f_of_g2_n))
#     check_f_of_g = list(map(lambda s1,s2 : sp.simplify(s1-s2), f_of_g1, f_of_g2))
#     print('Composition rule check: ', check_f_of_g)
    

    
    