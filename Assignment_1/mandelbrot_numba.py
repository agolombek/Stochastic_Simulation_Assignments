import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import MaxNLocator
from matplotlib import cm


@njit
def mandelbrot2(c,iterations):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iterations:
        z = z*z + c
        n += 1

    if n == iterations:
        return 1
    else:
        return 0
    

@njit
def mandelbrot_area(iterations,samples):

  counter = 0
  for i in range(samples):
    c = complex(np.random.uniform(-2,0.75),np.random.uniform(-1.25,1.25))
    m = mandelbrot2(c,iterations)
    counter += m
    
  return abs(2.75 * 2.5 * counter/samples)

"""Plot Area of Mandelbrot set"""

start_time = time()
print(mandelbrot_area(10000,10000))
end_time = time()
print(end_time-start_time)




