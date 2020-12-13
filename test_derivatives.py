#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 20:49:59 2020

@author: basile
"""

#import pyximport; pyximport.install()

import numpy as np
import sympy as sp

import derivatives_rules as proquo
import power_series_rules as proquo_r
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

def rescale_derivatives(f):
    fr = f.copy()
    fac = 1
    for k in range(len(f)):
        fr[k] /= fac
        fac *= k + 1
    return fr

def retrieve_derivatives(f):
    fr = f.copy()
    fac = 1
    for k in range(len(f)):
        fr[k] *= fac
        fac *= k + 1
    return fr

n = 4
x = sp.symbols('x')
# derivatives of f(x) w.r.t x
f = derivatives_list(sp.atan(x), x, n)    
# derivatives of g(x) w.r.t. x
g = derivatives_list(sp.ln(x), x, n)

# Product rule check
# Compute product derivatives with sympy directly
fg1 = derivatives_list(f[0] * g[0], x, n)
# Compute product derivatives using product_rule()
fg2 = proquo.product_rule(f,g)
check_fg = list(map(lambda s1,s2 : sp.simplify(s1-s2), fg1, fg2))
print('Product rule check: ', check_fg)

# Rescaled product rule
fgr = retrieve_derivatives(
    proquo_r.product_rule_r(rescale_derivatives(f), rescale_derivatives(g)))
check_fgr = list(map(lambda s1,s2 : sp.simplify(s1-s2), fg1, fgr))
print('Product rule check rescaled: ', check_fgr)

# Reciprocal rule check
# Compute reciprocal derivatives with sympy directly
rf1 = derivatives_list(1/f[0], x, n)
# Compute product derivatives using product_rule()
rf2 = proquo.reciprocal_rule(f)
check_rf = list(map(lambda s1,s2 : sp.simplify(s1-s2), rf1, rf2))
print('Reciprocal rule check: ', check_rf)

# Rescaled reciprocal rule
rfr = retrieve_derivatives(
    proquo_r.reciprocal_rule_r(rescale_derivatives(f)))
check_rfr = list(map(lambda s1,s2 : sp.simplify(s1-s2), rf1, rfr))
print('Reciprocal rule check rescaled: ', check_rfr)


# Quotient rule check
# Compute quotient derivatives with sympy directly
qfg1 = derivatives_list(f[0] / g[0], x, n)
# Compute quotient derivatives using quotient_rule()
qfg2 = proquo.quotient_rule(f,g)
check_qfg = list(map(lambda s1,s2 : sp.simplify(s1-s2), qfg1, qfg2))
print('Quotient rule check: ', check_qfg)

# Rescaled quotient rule
qfgr = retrieve_derivatives(
    proquo_r.quotient_rule_r(rescale_derivatives(f), rescale_derivatives(g)))
check_qfgr = list(map(lambda s1,s2 : sp.simplify(s1-s2), qfg1, qfgr))
print('Quotient rule check rescaled: ', check_qfgr)


# Composite derivatives check
# derivatives of f(x) w.r.t. x evaluated at x=g(x)
f_at_g = list(map(lambda y : y.subs(x,g[0]), f))
# devivatives of f(g(x)) w.r.t to x using sympy direcly
f_of_g1 = derivatives_list(f_at_g[0], x, n)

# n-th devivative of f(g(x)) w.r.t to x using Faa di Bruno
f_of_g2_n = proquo.composition_rule_nth(f_at_g[1:], g[1:])
# all devivatives of f(g(x)) w.r.t to x using Faa di Bruno
f_of_g2 = proquo.composition_rule(f_at_g, g)
print('n-th composite derivative check (Faa di Bruno)     : ', sp.simplify(f_of_g1[-1]-f_of_g2_n))
check_f_of_g = list(map(lambda s1,s2 : sp.simplify(s1-s2), f_of_g1, f_of_g2))
print('Composition rule check (Faa di Bruno)              : ', check_f_of_g)

# all devivatives of f(g(x)) w.r.t to x using truncated power series
f_of_g3 = trunc.composition_rule(f_at_g, g)
check_f_of_g3 = list(map(lambda s1,s2 : sp.simplify(s1-s2), f_of_g1, f_of_g3))
print('Composition rule check: (truncated power series)   : ', check_f_of_g)


# all devivatives of f(g(x)) w.r.t to x using rescaled truncated power series
f_of_gr = retrieve_derivatives(
    proquo_r.composition_rule_r(rescale_derivatives(f_at_g), rescale_derivatives(g)))
check_f_of_gr = list(map(lambda s1,s2 : sp.simplify(s1-s2), f_of_g1, f_of_gr))
print('Composition rule check: (rescaled power series)   : ', check_f_of_gr)


   
    