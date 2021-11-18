# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 14:22:12 2021

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
x_values = np.logspace(2, 5, 3) 
sample_range_sqrt = [100,200,300,400,500,1000]
sample_range = [100,200,300]
ortho = sampling(sample_range_sqrt,orthogonal_sampling)
latin = sampling(sample_range,latin_hypercube_sampling)
random = sampling(sample_range,random_sampling)
        
answer = Mandelbrot_Area(x_values, x_values, 1e-3,orthogonal_sampling)

iterations = answer[:,0]
samples = answer[:,1]
area = answer[:,2]
bootstrap_it = answer[:,3]
         
end_time = time()

print('The runtime was', (end_time-start_time)/(60*60), 'hours')   

############################# 3D PLOTTING ###################################

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_trisurf(np.log10(iterations),np.log10(samples), np.absolute(area-1.506484), linewidth=0, antialiased=True,cmap=cm.jet)
ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))
ax.tick_params(labelsize=16)
ax.set_xlabel(r'$Iterations$ ', fontsize=20, rotation=150)
ax.set_ylabel(r'$Samples$', fontsize=20)
ax.set_zlabel(r'$|A_{i,s} - A_M|$', fontsize=20, rotation=60)
plt.show()
fig.savefig("random")

