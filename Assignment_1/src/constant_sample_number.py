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

sample_range_sqrt = np.logspace(0.5,1,2)
x_values = np.logspace(1, 2, 20)


for sample_size_sqrt in [10,100,300,500]:

    print(orthogonal_sampling(int(sample_size_sqrt)))
    sample_size = int(sample_size_sqrt ** 2) 
    fig, ax = plt.subplots()
    
    ##################### Randome sampling ##################################
    title = str(int(sample_size)) + ' Samples'
    
    # answer = Mandelbrot_constant_samplesize(x_values, sample_size, 1e-3, random_sampling)
    # iterations = answer[:,0]
    # area = answer[:,1] 
    # error = abs(area - 1.506484193)
    # ax.plot(iterations, error, label='Random sampling') 
    
    # #################### Hypercube sampling ##################################
        
    # answer = Mandelbrot_constant_samplesize(x_values, sample_size, 1e-3, latin_hypercube_sampling)
    # iterations = answer[:,0]
    # area = answer[:,1]
    # error = abs(area - 1.506484193)
    # ax.plot(iterations, error, label='Hypercube sampling')

    #################### Orthogonal sampling ##################################

    answer = Mandelbrot_constant_samplesize(x_values, int(sample_size_sqrt), 1e-3, orthogonal_sampling)
    iterations = answer[:,0]
    area = answer[:,1]
    error = abs(area - 1.506484193)
    ax.plot(iterations, error, label='Orthogonal sampling')

    # # Finish Plot
    # ax.grid(axis='both')
    # ax.set_xscale('log')
    # ax.set_xlabel('Iterations')
    # ax.set_ylabel('Error')
    # ax.legend()
    # ax.set_title(title)
    # plt.show()
    
end_time = time()

print('The runtime was', (end_time-start_time)/(60*60), 'hours')  
