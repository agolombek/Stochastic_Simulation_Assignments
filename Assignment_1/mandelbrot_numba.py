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
    
  return abs(2.75 * 2.5 * counter/samples - 1.506484193)

"""Plot Area of Mandelbrot set"""

start_time = time()
print(mandelbrot_area(100000,1000000))
end_time = time()

print(end_time-start_time)


@njit 
def plot_values(start_it, stop_it, start_samp, stop_samp, div):
    x_values = np.linspace(start_it, stop_it, div)
    y_values = np.linspace(start_samp, stop_samp, div)
    calculations = np.square(x_values.size)
    answer = np.zeros((calculations, 3))
    i = 0
    for it in x_values:
        for samp in y_values:
            m = mandelbrot_area(int(it), int(samp))
            answer[i,0] = int(it)
            answer[i,1] = int(samp)
            answer[i,2] = m
            i += 1
    
    iterations = answer[:,0]
    samples = answer[:,1]
    area = answer[:,2]
    return iterations, samples, area
            

# start_time = time()          
# iterations, samples, area = plot_values(100, 1000, 10000, 1000000, 25)           
# end_time = time()

# print(end_time-start_time)   
    
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_trisurf(iterations,samples, area, linewidth=0, antialiased=True,cmap=cm.jet)
# ax.xaxis.set_major_locator(MaxNLocator(5))
# ax.yaxis.set_major_locator(MaxNLocator(6))
# ax.zaxis.set_major_locator(MaxNLocator(5))
# ax.tick_params(labelsize=16)
# ax.set_xlabel(r'$Iterations$ ', fontsize=20, rotation=150)
# ax.set_ylabel(r'$Samples$', fontsize=20)
# ax.set_zlabel(r'$Area$', fontsize=20, rotation=60)

