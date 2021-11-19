# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:14:26 2021

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

########################## CALLING AREA FUNCTION #############################
start_time = time() 
# using the sqrt because we need to use that for the orthogonal sampling

x_values = np.logspace(2, 5, 20)
sample_range_sqrt = [200,100]
sample_range = [200**2,100**2]
ortho = sampling(sample_range_sqrt,orthogonal_sampling)
latin = sampling(sample_range,latin_hypercube_sampling)
random = sampling(sample_range,random_sampling)

for i in range(len(sample_range)):

    fig, ax = plt.subplots()
    
    ##################### Randome sampling ##################################
    title = str(int(random[i].size/2)) + ' Samples'
    
    answer = Mandelbrot_constant_samplesize(x_values, random[i], 1e-3)
    iterations = answer[:,0]
    area = answer[:,1] 
    error = abs(area - area[-1])
    ax.plot(iterations, error, label='Random sampling') 
    
    # #################### Hypercube sampling ##################################
        
    answer = Mandelbrot_constant_samplesize(x_values, latin[i], 1e-3)
    iterations = answer[:,0]
    area = answer[:,1]
    error = abs(area - area[-1])
    ax.plot(iterations, error, label='Hypercube sampling')

    #################### Orthogonal sampling ##################################

    answer = Mandelbrot_constant_samplesize(x_values, ortho[i], 1e-3)
    iterations = answer[:,0]
    area = answer[:,1]
    error = abs(area - area[-1])
    ax.plot(iterations, error, label='Orthogonal sampling')

    # # Finish Plot
    ax.grid(axis='both')
    ax.set_xscale('log')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Error')
    ax.legend()
    ax.set_title(title)
    plt.show()
    
end_time = time()

print('The runtime was', (end_time-start_time)/(60*60), 'hours')  
