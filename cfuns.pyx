# cython: language_level=3, boundscheck=False, overflowcheck=False, cdivision=True
"""
Created on Fri Nov 27 16:22:24 2020

@author: basile
"""
from cpython cimport array
import array

# Binomial coefficients
# from https://gist.github.com/rougier/ebe734dcc6f4ff450abf
# Faster than scipy.special.binom
cdef int binomial_c(int n, int k):
    cdef int b, t
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
cdef double bell_c(int n, int k, double[:] x):
    """
    Evaluate the partial exponential Bell polynomial B_n,k(x)
    """
    cdef int i
    cdef double b, c
    if (n==0) & (k==0):
        return 1.0
    elif (k==0) | (n==0):
        return 0.0
    else:
        b = 0.0
        for i in range(n-k+1): 
            b += binomial_c(n-1, i) * x[i] * bell_c(n-i-1, k-1, x)
        return b
    
# Wrapper for binomial_c, should be used only for testing
def binomial(n, k):
    return binomial_c(n,k)

# Wrapper for bell_c with overhead only once
# https://docs.cython.org/en/latest/src/tutorial/array.html
# https://docs.python.org/3/library/array.html
def bell(int n, int k, xx):
    cdef array.array x = array.array('d', xx)
    cdef double[:] cx = x;
    assert len(xx) >= n-k+1, "Array x is too short. Length should be at least n-k+1"
    return bell_c(n, k, cx)

    