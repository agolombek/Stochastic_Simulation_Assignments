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
x_values = np.logspace(2, 5, 15)
sample_range_sqrt = [100,200,300,400,500,700,1000,1200]
sample_range = [100**2,200**2,300**2,400**2,500**2,700**2,1000**2,1200**2]
ortho = sampling(sample_range_sqrt,orthogonal_sampling)
latin = sampling(sample_range,latin_hypercube_sampling)
random = sampling(sample_range,random_sampling)
x = []
y = []
z = []

for i in range(len(sample_range)):

    answer = Mandelbrot_constant_samplesize(x_values, ortho[i], 1e-3)
    area = answer[:,1] 
    x = np.concatenate((x, x_values), axis=None)
    y = np.concatenate((y, [len(ortho[i]) for j in range(len(x_values))]), axis=None)
    z = np.concatenate((z, area), axis=None)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_trisurf(np.log10(x),np.log10(y), np.absolute(z-1.506484), linewidth=0, antialiased=True,cmap=cm.jet)
ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))
ax.tick_params(labelsize=16)
ax.set_xlabel(r'$log_{10}(Iterations)$ ', fontsize=14, rotation=150)
ax.set_ylabel(r'$log_{10}(Samples)$', fontsize=14)
ax.set_zlabel(r'$|A_{i,s} - A_M|$', fontsize=14, rotation=60)
plt.show()
    
    
