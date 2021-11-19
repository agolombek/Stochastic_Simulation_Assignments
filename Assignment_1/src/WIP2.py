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

all_iterations = np.logspace(2, 4, 30)
sqrt_sample_size = 100
max_std = 1e-3

answer = real_value_convergence(all_iterations, sqrt_sample_size, max_std)

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

    
    
    