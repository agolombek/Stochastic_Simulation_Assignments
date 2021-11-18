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


################# ITERATIVE MANDELBROT AREA FUNCTION #########################

def sampling(sample_size,sampling_function):
    sampling = []
    for size in sample_size:
        sampling.append(sampling_function(size))
    return np.array(sampling,dtype=object)



@njit
def Mandelbrot_Area(x_values, y_values, max_std, sampling_function):
    """
    This functions estimates the area of the mandelbrot set over a grid of 
    varying iterations and sample sizes, given a ceratin sampling function.
    --------------------------------------------------------------------------
    The argument x_values is an array containing all the numbers of iterations 
    each point in the sample space is tested for divergence.
    
    The argument y_values represents the sample sizes to be tested. Together
    with x_vbalues it forms the grid over which all values for which the 
    Mandelbrot set area is estimated. x_values and y_values must be arrays of
    equal size.
    
    max_std represents the maximum standrad deviation allowed for each point 
    in the grid. It thus represents the level of confidence in the result for
    each point in the grid.
    
    The sampling_function argument needs to be a function which return the 
    sample space in the form of n by 2 matrix with n points containing the x
    and y coordinate of each point.
    --------------------------------------------------------------------------
    The function returns the matrix answer with 4 columns. The first contains 
    the number of iterations each point in the sample was chekced for 
    divergence. The second contains the size of the sample, hence the number 
    of sample points. The third column contains the area estimnate. The fourth
    column contains the number of iterations of the bootstrap method which
    were preformed to lower the standard deviation below max_std.
    """
    # create a matrix with space for all grid_points and 4 columns
    answer = np.zeros((x_values.size**2, 4))
    # grid_point keeps track of the solution currently being investigated
    grid_point = 0
    # iterate through the number of iterations each point in sample is checked
    # for convergence
    for x in x_values:
        # iterate through all sample sizes
        for samp in y_values:
            # test all the points in the sample x times for convergence
            # generating the sample using the sampling function
            sample = sampling_function(int(samp))
            points = mandelbrot(sample, int(x), int(samp))
            # returns array of 0s and 1s. 1 represents the point being in the 
            # mandelbrot set, while 0 represents divergence. 
            # Area estimate is thus given by sum of this array multiplied by 
            # the area the sample was taken from.
            A = np.mean(points)*(2.75*2.5)
            # Initialize values for bootstrapping method
            S = 0
            n = 0
            std = 1
            l = 1
            # preform bootstrapping method at least 100 times and until the 
            # standard deviation is lower than max_std.
            while std > max_std or l < 100:
                
                #preform bootstrapping
                counter = 0
                for i in range(int(samp)):
                    counter += np.random.choice(points)
                    
                area_bootstrapping = (2.75*2.5)*counter/samp
                # Update Area and standrad deviation
                l += 1
                S = ((l-2)/(l-1))*S+(area_bootstrapping-A)**2/l
                A = (area_bootstrapping+(l-1)*A)/l
                n += 1
                std = 1.96*np.sqrt(S/(n))

            # Save location on grid, Area estimate and necessray bootstrapping
            # iterations in answer matrix
            answer[grid_point,0] = int(x)
            answer[grid_point,1] = int(samp)
            answer[grid_point,2] = A
            answer[grid_point,3] = l
            grid_point += 1
    
    return answer

# start_time = time() 
# x_values = np.logspace(2, 5, 3) 
# sample_range_sqrt = [100,200,300,400,500,1000]
# sample_range = [100,200,300]
# ortho = sampling(sample_range_sqrt,orthogonal_sampling)
# latin = sampling(sample_range,latin_hypercube_sampling)
# random = sampling(sample_range,random_sampling)
        
# answer = Mandelbrot_Area(x_values, [100,200,300], 1e-3,random_sampling)
# print(answer)


@njit
def Mandelbrot_constant_samplesize(x_values, sample, max_std):
    """
    This functions estimates the area of the mandelbrot set for a range of 
    iterations given a certain sample size a ceratin sampling function.
    --------------------------------------------------------------------------
    The argument x_values is an array containing all the numbers of iterations 
    each point in the sample space is tested for divergence.
    
    The argument ysample_size represents the number of samples drawn from the
    sample space.
    
    max_std represents the maximum standrad deviation allowed for each point 
    in the grid. It thus represents the level of confidence in the result for
    each point in the grid.
    
    The sampling_function argument needs to be a function which return the 
    sample space in the form of n by 2 matrix with n points containing the x
    and y coordinate of each point.
    --------------------------------------------------------------------------
    The function returns the matrix answer with 3 columns. The first contains 
    the number of iterations each point in the sample was chekced for 
    divergence. The second column contains the area estimnate. The third
    column contains the number of iterations of the bootstrap method which
    were preformed to lower the standard deviation below max_std.
    """
    # create a matrix with space for all grid_points and 4 columns
    answer = np.zeros((x_values.size, 3))
    # grid_point keeps track of the solution currently being investigated
    grid_point = 0
    # iterate through the number of iterations each point in sample is checked
    # for convergence
    for x in x_values:
        # test all the points in the sample x times for convergence
        points = mandelbrot(sample, int(x), int(sample.size/2))
        # returns array of 0s and 1s. 1 represents the point being in the 
        # mandelbrot set, while 0 represents divergence. 
        # Area estimate is thus given by sum of this array multiplied by 
        # the area the sample was taken from.
        A = np.mean(points)*(2.75*2.5)
        # Initialize values for bootstrapping method
        S = 0
        n = 0
        std = 1
        l = 1
        # preform bootstrapping method at least 100 times and until the 
        # standard deviation is lower than max_std.
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

        answer[grid_point,0] = int(x)
        answer[grid_point,1] = A
        answer[grid_point,2] = l
        grid_point += 1
    
    return answer








