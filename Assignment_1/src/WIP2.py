# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 13:34:26 2021

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

@njit
def function_convergence(all_iterations, sqrt_sample_size, max_std):
    answer = np.zeros((all_iterations.size, 4))
    grid_point = 0
    for iteration in all_iterations:
        sample_size = int(sqrt_sample_size**2)
        random_sample = random_sampling(int(sqrt_sample_size))
        hypercube_sample = latin_hypercube_sampling(int(sqrt_sample_size))
        ortho_sample = orthogonal_sampling(int(sqrt_sample_size))
        
        Area_random, bootstrap_itr1 = Mandelbrot_Area(int(iteration), random_sample, max_std)
        Area_hypercube, bootstrap_itr2 = Mandelbrot_Area(int(iteration), hypercube_sample, max_std)
        Area_ortho, bootstrap_itr3 = Mandelbrot_Area(int(iteration), ortho_sample, max_std)
        
        
        answer[grid_point,0] = int(iteration)
        answer[grid_point,1] = Area_random
        answer[grid_point,2] = Area_hypercube
        answer[grid_point,3] = Area_ortho
        grid_point += 1
    
    
    answer[:,1] = np.absolute(answer[:,1] - answer[-1,1])
    answer[:,2] = np.absolute(answer[:,2] - answer[-1,2])
    answer[:,3] = np.absolute(answer[:,3] - answer[-1,3])
    return answer

@njit
def real_value_convergence(all_iterations, sqrt_sample_size, max_std):
    answer = np.zeros((all_iterations.size, 4))
    grid_point = 0
    for iteration in all_iterations:
        sample_size = int(sqrt_sample_size**2)
        random_sample = random_sampling(int(sqrt_sample_size))
        hypercube_sample = latin_hypercube_sampling(int(sqrt_sample_size))
        ortho_sample = orthogonal_sampling(int(sqrt_sample_size))
        
        Area_random, bootstrap_itr1 = Mandelbrot_Area(int(iteration), random_sample, max_std)
        Area_hypercube, bootstrap_itr2 = Mandelbrot_Area(int(iteration), hypercube_sample, max_std)
        Area_ortho, bootstrap_itr3 = Mandelbrot_Area(int(iteration), ortho_sample, max_std)
        
        
        answer[grid_point,0] = int(iteration)
        answer[grid_point,1] = Area_random
        answer[grid_point,2] = Area_hypercube
        answer[grid_point,3] = Area_ortho
        grid_point += 1
    
    real_area = 1.506484193
    answer[:,1] = np.absolute(answer[:,1] - real_area)
    answer[:,2] = np.absolute(answer[:,2] - real_area)
    answer[:,3] = np.absolute(answer[:,3] - real_area)
    return answer


start_time = time() 

all_iterations = np.logspace(2, 4, 30)
sqrt_sample_size = 100
max_std = 1e-3

answer = function_convergence(all_iterations, sqrt_sample_size, max_std)

ITERATIONS= answer[:,0]
ERROR_RANDOM= answer[:,1]
ERROR_HYPERCUBE = answer[:,2]
ERROR_ORTHO = answer[:,3]

end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours')  

############################## PLOTTING #####################################

fig, ax = plt.subplots()
    
##################### Randome sampling ##################################
title = str(int(sqrt_sample_size**2)) + ' Samples'

ax.plot(ITERATIONS, ERROR_RANDOM, label='Random sampling') 
ax.plot(ITERATIONS, ERROR_HYPERCUBE, label='Hypercube sampling')
ax.plot(ITERATIONS, ERROR_ORTHO, label='Orthogonal sampling')

# # Finish Plot
ax.grid(axis='both')
ax.set_xscale('log')
ax.set_xlabel('Iterations')
ax.set_ylabel('Error')
ax.legend()
ax.set_title(title)
plt.show()

    
    
    