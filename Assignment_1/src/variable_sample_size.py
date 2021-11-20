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

all_iterations = np.logspace(2, 5, 20)
all_sqrt_sample_sizes = np.logspace(2, 3.5, 20)
max_std = 1e-3

method = latin_hypercube_sampling

answer = iteration_function(all_iterations, all_sqrt_sample_sizes, max_std, method)

AREAS = answer[:,0]
ITERATIONS = answer[:,1]
SAMPLE_SIZE = answer[:,2]
BOOTSTRAP_ITERATIONS = answer[:,3]

real_area =  1.506484193
ERROR = np.absolute(AREAS - real_area)


end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours') 
print(AREAS[-1]) 

############################## PLOTTING #####################################
     
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
    
    
