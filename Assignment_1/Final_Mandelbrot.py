# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:25:00 2021

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

######################### MANDELBROT ITERATIONS ##############################

@njit
def mandelbrot(points, iterations, size):
    """
    This function analyzes a range of values for whether they are part of the 
    mandelbrot set or not.
    --------------------------------------------------------------------------
    The first argument is the x and y values of the points to be tested in the 
    form of a n by 2 matrix with n being the number of points to be tested.
    
    The iterations argument is an integer value representing the number of 
    times a point is iterated over before it is concluded whether it is in the
    mandelbrot set or not.
    
    The size is the number of points, this is required to generate the answer 
    array to comply with the format to allow efficient numba implementation.
    --------------------------------------------------------------------------
    The fuction returns an array of 0 and 1 with a 1 indicating that the point 
    at that index is part of the mandelbrot set, while a 0 indicates that it 
    diverged and is thus not part of the set.
    """
    answer = np.zeros(size)
    i = 0
    for c in points:
        z = 0
        n = 0
        while abs(z) <= 2 and n < iterations:
            z = z*z + complex(c[0], c[1])
            n += 1

        if n == iterations:
            answer[i] = 1
  
        i += 1
    return answer

######################### SAMPLING METHODS ###################################

@njit
def random_sampling(samp_size):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using the random sampling method.
    --------------------------------------------------------------------------
    The function argument is the number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    sample_space = np.zeros((samp_size, 2))
    for i in range(samp_size):
        sample_space[i, 0] = np.random.uniform(-2,0.75)
        sample_space[i, 1] = np.random.uniform(-1.25,1.25)
    return sample_space

@njit
def latin_hypercube_sampling(samp_size):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using the latin hypercube sampling 
    method.
    --------------------------------------------------------------------------
    The function argument is the number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    sample_space = np.zeros((samp_size, 2))
    perm1 = np.random.permutation(samp_size)
    perm2 = np.random.permutation(samp_size)
    for i in range(samp_size):
        sample_space[i, 0] = ((np.random.random()+perm1[i])/samp_size)*2.75-0.75
        sample_space[i, 1] = ((np.random.random()+perm2[i])/samp_size)*2.5-1.25
    return sample_space


################# ITERATIVE MANDELBROT AREA FUNCTION #########################

@njit
def plot_values(x_values, y_values, max_std, sampling_function):
    """
    This functions estimates the area of the mandelbrot set over a grid of 
    varying iterations and sample sizes, given a ceratin sampling function.
    --------------------------------------------------------------------------
    The argument x_values is an array containing all the numbers of iterations 
    each point in the sample space is tested for divergence.
    
    The argument y_values represents the sample sizes to be tested. Together
    with x_vbalues it forms the grid over which all values for which the 
    Mandelbrot set area is estimated. 
    
    max_std represents the maximum standrad deviation allowed for each point 
    in the grid. It thus represents the level of confidence in the result.
    """
    steps = x_values.size
    answer = np.zeros((steps**2, 4))
    grid_point = 0
    # sam = sampling_function(y_values[0])
    for it in x_values:
        for samp in y_values:
            #generating the sample with this value of it and samp
            sample = sampling_function(int(samp))
            #testing all the points and putting them inside an array
            # 1 if the point is inside, 0 otherwise
            points = mandelbrot(sample, int(it), int(samp))
            A = np.mean(points)*(2.75*2.5)
            S = 0
            n = 0
            std = 1
            l = 1
            while std > max_std or l < 100:
                
                # randomly picking samp points with replacement
                counter = 0
                for i in range(int(samp)):
                    counter += np.random.choice(points)
                area_bootstrapping = (2.75*2.5)*counter/samp
                l += 1
                S = ((l-2)/(l-1))*S+(area_bootstrapping-A)**2/l
                A = (area_bootstrapping+(l-1)*A)/l
                n += 1
                std = 1.96*np.sqrt(S/(n))

            # append point to answer 
            answer[grid_point,0] = int(it)
            answer[grid_point,1] = int(samp)
            answer[grid_point,2] = A
            answer[grid_point,3] = l
            grid_point += 1
    
    return answer

x_values = np.logspace(3, 5, 5)
y_values = np.logspace(3, 5, 5)
answer,all_samples = plot_values(x_values, y_values, 1e-3, latin_hypercube_sampling)

for [x, y] in all_samples:
    plt.plot(x, y,"r.")

plt.show()

########################## CALLING AREA FUNCTION #############################

# start_time = time()  
     
# x_values = np.logspace(4, 5, 10)
# y_values = np.logspace(4, 5, 10)
        
# answer = plot_values(x_values, y_values, 1e-3, latin_hypercube_sampling) 

# iterations = answer[:,0]
# samples = answer[:,1]
# area = answer[:,2]
# bootstrap_it = answer[:,3]
         
# end_time = time()

# print('The runtime was', (end_time-start_time)/(60*60), 'hours')   

# ############################# 3D PLOTTING ###################################

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_trisurf(iterations,samples, area, linewidth=0, antialiased=True,cmap=cm.jet)
# ax.xaxis.set_major_locator(MaxNLocator(5))
# ax.yaxis.set_major_locator(MaxNLocator(6))
# ax.zaxis.set_major_locator(MaxNLocator(5))
# ax.tick_params(labelsize=16)
# ax.set_xlabel(r'$Iterations$ ', fontsize=20, rotation=150)
# ax.set_ylabel(r'$Samples$', fontsize=20)
# ax.set_zlabel(r'$Area$', fontsize=20, rotation=60)
# plt.show()









