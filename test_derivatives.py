#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:49:59 2020

@author: basile
"""

import numpy as np
import sympy as sp

import product_quotient_rules as proquo
import faa_di_bruno as bruno
import truncated_power_series as trunc

def nest_list(f,x,n):
    fx = [0] * (n+1)
    fx[0] = x
    for k in range(n):
        fx[k+1] = f(fx[k])
    return fx

def derivatives_list(s,x,n):
    f = lambda expr : sp.diff(expr, x)
    return nest_list(f,s,n)

n = 4
x = sp.symbols('x')
# derivatives of f(x) w.r.t x
f = derivatives_list(sp.atan(x), x, n)    
# derivatives of g(x) w.r.t. x
g = derivatives_list(sp.ln(x), x, n)

# Product rule check
# Compute product derivatives with sympy directly
fg1 = derivatives_list(f[0] * g[0], x, n)
# Compute prodeuct derivatives using product_rule()
fg2 = proquo.product_rule(f,g)
check_fg = list(map(lambda s1,s2 : sp.simplify(s1-s2), fg1, fg2))
print('Product rule check: ', check_fg)

# Reciprocal rule check
# Compute reciprocal derivatives with sympy directly
rf1 = derivatives_list(1/f[0], x, n)
# Compute product derivatives using product_rule()
rf2 = proquo.reciprocal_rule(f)
check_rf = list(map(lambda s1,s2 : sp.simplify(s1-s2), rf1, rf2))
print('Reciprocal rule check: ', check_rf)

# Quotient rule check
# Compute quotient derivatives with sympy directly
qfg1 = derivatives_list(f[0] / g[0], x, n)
# Compute quotient derivatives using quotient_rule()
qfg2 = proquo.quotient_rule(f,g)
check_qfg = list(map(lambda s1,s2 : sp.simplify(s1-s2), qfg1, qfg2))
print('Quotient rule check: ', check_qfg)


# Composite derivatives check
# derivatives of f(x) w.r.t. x evaluated at x=g(x)
f_at_g = list(map(lambda y : y.subs(x,g[0]), f))
# devivatives of f(g(x)) w.r.t to x using sympy direcly
f_of_g1 = derivatives_list(f_at_g[0], x, n)

# n-th devivative of f(g(x)) w.r.t to x using Faa di Bruno
f_of_g2_n = bruno.composition_rule_nth(f_at_g[1:], g[1:])
# all devivatives of f(g(x)) w.r.t to x using Faa di Bruno
f_of_g2 = bruno.composition_rule(f_at_g, g)
print('n-th composite derivative check (Faa di Bruno)     : ', sp.simplify(f_of_g1[-1]-f_of_g2_n))
check_f_of_g = list(map(lambda s1,s2 : sp.simplify(s1-s2), f_of_g1, f_of_g2))
print('Composition rule check (Faa di Bruno)              : ', check_f_of_g)

# all devivatives of f(g(x)) w.r.t to x using truncated power series
f_of_g3 = trunc.composition_rule(f_at_g, g)
check_f_of_g3 = list(map(lambda s1,s2 : sp.simplify(s1-s2), f_of_g1, f_of_g3))
print('Composition rule check: (truncated power series)   : ', check_f_of_g)


   
    