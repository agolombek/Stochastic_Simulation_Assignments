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



@njit
def optimized_mandelbrot(points,iterations, c = 1):

    # the new variable will be X - c * (Y - u_Y) where Y is 1 if the point is inside the semicircle
    # centered in -0.25 and with radius 0.5, 0 otherwise. The expected value will be pi*0.5**2/2

    answer = np.zeros(int(points.size/2))
    i = 0
    for c in points:

        z = 0
        n = 0

        while abs(z) <= 2 and n < iterations:
            z = z*z + complex(c[0]*2.75-2, c[1]*1.25)
            n += 1

        if (c[0]+0.25)**2+c[1]**2 < 0.025 and n == iterations:
            answer[i] = 0.39269908125

        elif n == iterations:
            answer[i] = 1

        elif (c[0]+0.25)**2+c[1]**2 < 0.025:
            answer[i] = 0.60730091875
  
        i += 1

    return answer



######################### SAMPLING METHODS ###################################

@njit
def random_sampling(samp_size_sqrt):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using the random sampling method.
    --------------------------------------------------------------------------
    The function argument is the root of number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    samp_size = int(samp_size_sqrt**2)
    sample_space = np.zeros((samp_size, 2))
    for i in range(samp_size):
        sample_space[i, 0] = np.random.uniform(-2,0.75)
        sample_space[i, 1] = np.random.uniform(-1.25,1.25)
    return sample_space

@njit
def latin_hypercube_sampling(samp_size_sqrt):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using the latin hypercube sampling 
    method.
    --------------------------------------------------------------------------
    The function argument is the root of number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    samp_size = int(samp_size_sqrt**2)
    sample_space = np.zeros((samp_size, 2))
    perm1 = np.random.permutation(samp_size)
    perm2 = np.random.permutation(samp_size)
    for i in range(samp_size):
        sample_space[i, 0] = ((np.random.random()+perm1[i])/samp_size)*2.75-2
        sample_space[i, 1] = ((np.random.random()+perm2[i])/samp_size)*2.5-1.25
    return sample_space

@njit
def orthogonal_sampling(major):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using orthogonal sampling.
    --------------------------------------------------------------------------
    The function argument is the square root of number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    #initialising the final array
    sample_space = np.zeros((major*major,2))
    #x values of the points
    col1 = np.zeros((major*major))
    col = np.zeros(major)
    for i in range(1,major+1):
        start_idx = (i-1)*major
        stop_idx = (i-1)*major+major
        col[0:major] = 0
        for j in range(1,major+1):
            col[j-1] = (i-1)*major+j
        col1[start_idx:stop_idx] = np.random.permutation(col)


    #y values of the points
    col2 = np.zeros((major*major))
    # changing the elements of the second column
    for j in range(major):
        for i in range(major):
            col2[i+major*j]=i+1
    for i in range(1,major+1):
        col[0:major] = 0
        for j in range(1,major+1):
            col[j-1] = (i-1)*major+j
        change = np.random.permutation(col)
        for j in range(major):
            col2[i-1+j*major] = change[j]
    for i in range(major*major):
        sample_space[i,0] = ((np.random.random()+col1[i]-1)/major**2)*2.75-2
        sample_space[i,1] = ((np.random.random()+col2[i]-1)/major**2)*2.5-1.25

    return sample_space


@njit
def orthogonal_sampling_01(major):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using orthogonal sampling.
    --------------------------------------------------------------------------
    The function argument is the square root of number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    #initialising the final array
    sample_space = np.zeros((major*major,2))
    #x values of the points
    col1 = np.zeros((major*major))
    col = np.zeros(major)
    for i in range(1,major+1):
        start_idx = (i-1)*major
        stop_idx = (i-1)*major+major
        col[0:major] = 0
        for j in range(1,major+1):
            col[j-1] = (i-1)*major+j
        col1[start_idx:stop_idx] = np.random.permutation(col)


    #y values of the points
    col2 = np.zeros((major*major))
    # changing the elements of the second column
    for j in range(major):
        for i in range(major):
            col2[i+major*j]=i+1
    for i in range(1,major+1):
        col[0:major] = 0
        for j in range(1,major+1):
            col[j-1] = (i-1)*major+j
        change = np.random.permutation(col)
        for j in range(major):
            col2[i-1+j*major] = change[j]
    for i in range(major*major):
        sample_space[i,0] = ((np.random.random()+col1[i]-1)/major**2)
        sample_space[i,1] = ((np.random.random()+col2[i]-1)/major**2)

    return sample_space
##################### MANDELBROT AREA FUNCTION ##############################

@njit
def Mandelbrot_Area(iterations, sample, max_std):

    points = mandelbrot(sample, iterations, int(sample.size/2))
    A = np.mean(points)*(2.75*2.5)
    S = 0
    n = 0
    std = 1
    l = 1
    
    while std > max_std or l < 100:
        #preform bootstrapping
        counter = 0
        for i in range(int(sample.size/2)):
            counter += np.random.choice(points)
        area_bootstrapping = (2.75*2.5)*counter/(sample.size/2)
        # Update Area and standrad deviation
        l += 1
        S = ((l-2)/(l-1))*S+(area_bootstrapping-A)**2/l
        A = (area_bootstrapping+(l-1)*A)/l
        n += 1
        std = 1.96*np.sqrt(S/(n))

    return A, n


@njit
def Mandelbrot_Area_improved(iterations, sample, max_std, c=1):

    points = optimized_mandelbrot(sample, iterations, c)
    A = np.mean(points)*(2.75*1.25)
    S = 0
    n = 0
    std = 1
    l = 1
    
    while std > max_std or l < 100:
        #preform bootstrapping
        counter = 0
        for i in range(int(sample.size/2)):
            counter += np.random.choice(points)
        area_bootstrapping = (2.75*1.25)*counter/(sample.size/2)
        # Update Area and standrad deviation
        l += 1
        S = ((l-2)/(l-1))*S+(area_bootstrapping-A)**2/l
        A = (area_bootstrapping+(l-1)*A)/l
        n += 1
        std = 1.96*2*np.sqrt(S/(n))

    return A*2, n

########################## ITERATIVE FUNCTIONS ###############################

@njit
def iteration_function(all_iterations, all_sqrt_sample_sizes, max_std, method):
    answer = np.zeros((all_iterations.size*all_sqrt_sample_sizes.size, 4))
    grid_point = 0
    for iteration in all_iterations:
        for sqrt_sample_size in all_sqrt_sample_sizes:
            sample_size = int(sqrt_sample_size**2)
            sample = method(int(sqrt_sample_size))
            # calculate area estimate 
            Area, bootstrap_itr = Mandelbrot_Area(int(iteration), sample, max_std)
            answer[grid_point,0] = Area
            answer[grid_point,1] = iteration
            answer[grid_point,2] = sample_size
            answer[grid_point,3] = bootstrap_itr
            grid_point += 1
    return answer

@njit
def function_convergence(all_iterations, sqrt_sample_size, max_std):
    answer = np.zeros((all_iterations.size, 4))
    grid_point = 0
    for iteration in all_iterations:
        sample_size = int(sqrt_sample_size**2)
        random_sample = random_sampling(int(sqrt_sample_size))
        hypercube_sample = latin_hypercube_sampling(int(sqrt_sample_size))
        ortho_sample = orthogonal_sampling(int(sqrt_sample_size))
        
        Area_random, bootstrap_itr1 = Mandelbrot_Area(int(iteration), random_sample, max_std)
        Area_hypercube, bootstrap_itr2 = Mandelbrot_Area(int(iteration), hypercube_sample, max_std)
        Area_ortho, bootstrap_itr3 = Mandelbrot_Area(int(iteration), ortho_sample, max_std)
        
        
        answer[grid_point,0] = int(iteration)
        answer[grid_point,1] = Area_random
        answer[grid_point,2] = Area_hypercube
        answer[grid_point,3] = Area_ortho
        grid_point += 1
    
    
    answer[:,1] = np.absolute(answer[:,1] - answer[-1,1])
    answer[:,2] = np.absolute(answer[:,2] - answer[-1,2])
    answer[:,3] = np.absolute(answer[:,3] - answer[-1,3])
    return answer

@njit
def real_value_convergence_test(all_iterations, sqrt_sample_size, max_std):
    answer = np.zeros((all_iterations.size, 5))
    grid_point = 0
    for iteration in all_iterations:
        sample_size = int(sqrt_sample_size**2)
        random_sample = random_sampling(int(sqrt_sample_size))
        hypercube_sample = latin_hypercube_sampling(int(sqrt_sample_size))
        ortho_sample = orthogonal_sampling(int(sqrt_sample_size))
        ortho_2 = orthogonal_sampling_01(int(sqrt_sample_size))
        
        Area_random, bootstrap_itr1 = Mandelbrot_Area(int(iteration), random_sample, max_std)
        Area_hypercube, bootstrap_itr2 = Mandelbrot_Area(int(iteration), hypercube_sample, max_std)
        Area_ortho, bootstrap_itr3 = Mandelbrot_Area(int(iteration), ortho_sample, max_std)
        Area_optimized, bootstrap_itr4 = Mandelbrot_Area_improved(int(iteration),ortho_2,max_std)
        
        answer[grid_point,0] = int(iteration)
        answer[grid_point,1] = Area_random
        answer[grid_point,2] = Area_hypercube
        answer[grid_point,3] = Area_ortho
        answer[grid_point,4] = Area_optimized
        grid_point += 1
    
    real_area = 1.506484193
    answer[:,1] = np.absolute(answer[:,1] - real_area)
    answer[:,2] = np.absolute(answer[:,2] - real_area)
    answer[:,3] = np.absolute(answer[:,3] - real_area)
    answer[:,4] = np.absolute(answer[:,4] - real_area)

    return answer