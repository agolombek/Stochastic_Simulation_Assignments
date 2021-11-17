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
sample_range = np.array([100, 1000])
x_values = np.logspace(2, 3, 5)

for sample_size in sample_range:
    
    ##################### Randome sampling ##################################
    title = str(sample_size) + ' Samples'
    
    answer = Mandelbrot_constant_samplesize(x_values, sample_size, 1e-3, random_sampling)
    iterations = answer[:,0]
    area = answer[:,1] 
    error = area - 1.506484193
    plt.plot(iterations, error, label='Random sampling') 
    
    #################### Hypercube sampling ##################################
    title = str(sample_size) + 'samples'
        
    answer = Mandelbrot_constant_samplesize(x_values, sample_size, 1e-3, latin_hypercube_sampling)
    iterations = answer[:,0]
    area = answer[:,1]
    error = area - 1.506484193
    plt.plot(iterations, error, label='Hypercube sampling')
    
    # Finish Plot
    plt.grid()
    plt.xscale('log')
    plt.xlabel('Iterations', fontsize=18)
    plt.ylabel('Error', fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=18)
    plt.title(title, fontsize=22)
    plt.savefig(title)
    
end_time = time()

print('The runtime was', (end_time-start_time)/(60*60), 'hours')  
