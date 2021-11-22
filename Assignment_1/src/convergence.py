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

start_time = time() 

all_iterations = np.logspace(2, 5, 30)
sqrt_sample_size = 400
max_std = 1e-3

answer = function_convergence(all_iterations, sqrt_sample_size, max_std)
#answer = real_value_convergence_test(all_iterations, sqrt_sample_size, max_std)


ITERATIONS= answer[:,0]
ERROR_RANDOM= answer[:,1]
ERROR_HYPERCUBE = answer[:,2]
ERROR_ORTHO = answer[:,3]
ERROR_OPTIM = answer[:,4]
bootstrap_itr1 = answer[:,5]
bootstrap_itr2 = answer[:,6]
bootstrap_itr3 = answer[:,7]
bootstrap_itr4 = answer[:,8]
means= [np.mean(bootstrap_itr1),np.mean(bootstrap_itr2),np.mean(bootstrap_itr3),np.mean(bootstrap_itr4)]
print(means)

end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours')  

############################## PLOTTING #####################################

fig, ax = plt.subplots()
    
##################### Randome sampling ##################################
title = str(int(sqrt_sample_size**2)) + ' Samples'

ax.plot(ITERATIONS, ERROR_RANDOM, label='Random sampling') 
ax.plot(ITERATIONS, ERROR_HYPERCUBE, label='Hypercube sampling')
ax.plot(ITERATIONS, ERROR_ORTHO, label='Orthogonal sampling')
ax.plot(ITERATIONS, ERROR_OPTIM, label='Optimized Montecarlo')

# # Finish Plot
ax.grid(axis='both')
ax.set_xscale('log')
ax.set_xlabel('Iterations')
ax.set_ylabel('Error')
ax.legend()
ax.set_title(title)
plt.show()


fig, ax = plt.subplots()
title = str(int(sqrt_sample_size**2)) + ' Samples'
ax.plot(ITERATIONS, bootstrap_itr1, label='Random sampling') 
ax.plot(ITERATIONS, bootstrap_itr2, label='Hypercube sampling')
ax.plot(ITERATIONS, bootstrap_itr3, label='Orthogonal sampling')
ax.plot(ITERATIONS, bootstrap_itr4, label='Optimized Montecarlo')
# # Finish Plot
ax.grid(axis='both')
ax.set_xscale('log')
ax.set_xlabel('Iterations')
ax.set_ylabel('bootstrapping iterations')
ax.legend()
ax.set_title(title)
plt.show()

    
    
    