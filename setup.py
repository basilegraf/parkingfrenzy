# cython: language_level=3, boundscheck=False, overflowcheck=False, cdivision=True

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(["cfuns.pyx", "power_series_rules_c.pyx"], annotate=True)
)
