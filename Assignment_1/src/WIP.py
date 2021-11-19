# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 12:48:56 2021

@author: arong
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from numba import njit
from time import time
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
from mandelbrot_functions import *


start_time = time() 

all_iterations = np.logspace(2, 3, 5)
all_sqrt_sample_sizes = np.logspace(1, 2, 5)

# Main Loop
real_area =  1.506484193
answer = np.zeros((all_iterations.size*all_sqrt_sample_sizes.size, 4))
grid_point = 0
for iteration in all_iterations:
    for sqrt_sample_size in all_sqrt_sample_sizes:
        sample_size = int(sqrt_sample_size**2)
        # create sample
        # sample = random_sampling(sample_size)
        # sample = latin_hypercube_sampling(sample_size)
        sample = orthogonal_sampling(int(sqrt_sample_size))
        # calculate area estimate 
        Area, bootstrap_itr = Mandelbrot_Area(int(iteration), sample, 1e-3)
        answer[grid_point,0] = Area
        answer[grid_point,1] = iteration
        answer[grid_point,2] = sample_size
        answer[grid_point,3] = bootstrap_itr
        grid_point += 1

AREAS = answer[:,0]
ITERATIONS = answer[:,1]
SAMPLE_SIZE = answer[:,2]
BOOTSTRAP_ITERATIONS = answer[:,3]

ERROR = np.absolute(AREAS - real_area)
  
end_time = time()       

print('The runtime was', (end_time-start_time)/(60*60), 'hours')  
        
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_trisurf(np.log10(ITERATIONS),np.log10(SAMPLE_SIZE), ERROR, linewidth=0, antialiased=True,cmap=cm.jet)
ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))
ax.tick_params(labelsize=16)
ax.set_xlabel(r'$log_{10}(Iterations)$ ', fontsize=14, rotation=150)
ax.set_ylabel(r'$log_{10}(Samples)$', fontsize=14)
ax.set_zlabel(r'$|A_{i,s} - A_M|$', fontsize=14, rotation=60)
plt.show()