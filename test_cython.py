#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 14:41:42 2020

@author: basile
"""

import numpy as np
import time

#import pyximport; pyximport.install()
from high_order_derivatives import addd

print(addd(5,2))

n=5
f = np.random.randn(n)
g = np.random.randn(n)

t0 = time.time()
#h=composition_rule(f, g)
t1 = time.time()

#print(h)
print('time = ', t1-t0)


def binomial_noc(n, k):
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
def bell_noc(n,k,x):
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
            b += binomial_noc(n-1, i) * x[i] * bell(n-i-1, k-1, x)
        return b

binomial(5,2)

nn = 150
res1 = [0] * nn
res2 = [0] * nn

t0 = time.time()
for k in range(nn):
    res1[k] = binomial(nn,k)
t1 = time.time()
print('time C binomial= ', t1-t0)

t0 = time.time()
for k in range(nn):
    res2[k] = binomial_noc(nn,k)
t1 = time.time()
print('time nonC binomial= ', t1-t0)

n=20
m=25
k=20
x = np.random.randn(m)
t0 = time.time()
bell(n,k,x)
t1 = time.time()
print('time bell = ', t1-t0)
t0 = time.time()
bell(n,k,x)
t1 = time.time()
print('time bell_noc = ', t1-t0)
