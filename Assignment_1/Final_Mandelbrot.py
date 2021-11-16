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

@njit
def mandelbrot(points, iterations, size):
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

@njit
def random_sampling(samp_size):
    answer = np.zeros((samp_size, 2))
    for i in range(samp_size):
        answer[i, 0] = np.random.uniform(-2,0.75)
        answer[i, 1] = np.random.uniform(-1.25,1.25)
    return answer
        

@njit
def plot_values(x_values, y_values, max_std, sampling_function):
    steps = x_values.size
    answer = np.zeros((steps**2, 4))
    Bbbboot = 0
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
                
                S = (1-1/l)*S+(1+l)*((area_bootstrapping-A)/l)**0.5
                
                A = A + (area_bootstrapping-A)/(l+1)
                n += 1
                std = 1.96*np.sqrt(S/(n))
                l += 1
                
            # append point to answer 
            answer[Bbbboot,0] = int(it)
            answer[Bbbboot,1] = int(samp)
            answer[Bbbboot,2] = A
            answer[Bbbboot,3] = l
            Bbbboot += 1
    
    iterations = answer[:,0]
    samples = answer[:,1]
    area = answer[:,2]
    bootstrap_it = answer[:,3]
    return iterations, samples, area, bootstrap_it
            
x_values = np.logspace(3, 5, 10)
y_values = np.logspace(3, 5, 10)


start_time = time()          
iterations, samples, area, bootstrap_it = plot_values(x_values, y_values, 1e-4, random_sampling)           
end_time = time()

print(end_time-start_time)   
    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_trisurf(iterations,samples, area, linewidth=0, antialiased=True,cmap=cm.jet)
ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(6))
ax.zaxis.set_major_locator(MaxNLocator(5))
ax.tick_params(labelsize=16)
ax.set_xlabel(r'$Iterations$ ', fontsize=20, rotation=150)
ax.set_ylabel(r'$Samples$', fontsize=20)
ax.set_zlabel(r'$Area$', fontsize=20, rotation=60)