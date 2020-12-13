#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 14:16:11 2020

@author: basile
"""

import numpy as np
import time

import pyximport; pyximport.install()
import power_series_rules_c as psrc
import power_series_rules as psr



f = np.array([1.0,2.0,3.0,4.0])
g = np.array([4.3,2.3,4.3,3.0])


h  = psr.product_rule_r(f, g)
hc = psrc.product_rule_r(f, g)

print("product rule:")
print(h)
print(hc)
print(hc-h)


h = psr.reciprocal_rule_r(f)
hc = psrc.reciprocal_rule_r(f)

print("reciprocal rule:")
print(h)
print(hc)
print(hc-h)


h  = psr.quotient_rule_r(f, g)
hc = psrc.quotient_rule_r(f, g)

print("quotient rule")
print(h)
print(hc)
print(hc-h)


h  = psr.poly_composition_rule_r(f, g)
hc = psrc.poly_composition_rule_r(f, g)

print("poly composition rule")
print(h)
print(hc)
print(hc-h)


h  = psr.composition_rule_r(f, g)
hc = psrc.composition_rule_r(f, g)

print("function composition rule")
print(h)
print(hc)
print(hc-h)


n = 20
f = np.random.randn(n)
g = np.random.randn(n)

t0 = time.time()
hc  = psrc.composition_rule_r(f, g)
t1c = time.time() - t0
print("time c: ", t1c)

t0 = time.time()
h  = psr.composition_rule_r(f, g)
t1p = time.time() - t0
print("time p: ", t1p)
print("Speedup = ", t1p/t1c)

print("Max relative diff: ", np.max(np.abs(hc-h)) / np.max(np.abs(h)))



