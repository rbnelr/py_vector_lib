from distutils.core import setup
from Cython.Build import cythonize

setup(name='cy_vectors', ext_modules=cythonize("cy_vectors.pyx"))
