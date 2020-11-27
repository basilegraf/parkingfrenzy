#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:24:09 2020

@author: basile
"""

#import numpy as np
#import time

#import pyximport; pyximport.install()

#import pyximport
#pyximport.install(reload_support=True)

import numpy as np
import time
import cfuns
import high_order_derivatives as hod


print(cfuns.binomial(5,2))
print(hod.binomial(5,2))


n=20

x=np.random.rand(n+1)

t0 = time.time()
bx_c = 0.0
for k in range(n+1):
    bx_c += cfuns.bell(n,k,x)
tc = time.time() - t0
print("c bell  : ", tc)

t0 = time.time()
bx_p = 0.0
for k in range(n+1):
    bx_p += hod.bell(n,k,x)
tp = time.time() - t0
print("p bell  : ", tp)
print("speedup :", tp/tc)

print(bx_c)
print(bx_c-bx_p)
