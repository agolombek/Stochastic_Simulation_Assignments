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
x_values = np.logspace(4, 5, 10)
sample_size = 1000000
        
answer = Mandelbrot_constant_samplesize(x_values, sample_size, 1e-3, random_sampling)

iterations = answer[:,0]
area = answer[:,2]
bootstrap_it = answer[:,3]
         
end_time = time()

print('The runtime was', (end_time-start_time)/(60*60), 'hours')   

############################# PLOTTING ######################################

