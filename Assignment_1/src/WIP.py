# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 11:29:51 2021

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


def orthogonal_sampling(major):
    """
    This function provides sample points for half open interval 
    x = [-.075, 2), y = [-1.25, 1.25) using the latin hypercube sampling 
    method.
    --------------------------------------------------------------------------
    The function argument is the square root of number of points to be sampled.
    --------------------------------------------------------------------------
    The function returns a n by 2 matrix with n being the number of points 
    to be tested, containing the x and y values in colum 1 and 2 respectively.  
    """
    #initialising the final array
    sample_space = np.zeros((major*major,2))

    #x values of the points
    col1 = np.array([])
    for i in range(1,major+1):
        for j in range(1,major+1):
            col1 = np.append(col1,np.random.permutation([(i-1)*major+j])

    #y values of the points
    col2 = np.zeros((major*major))
    # changing the elements of the second column
    for j in range(major):
        for i in range(major):
            col2[i+major*j]=i+1
    for i in range(1,major+1):
        change = np.random.permutation([(i-1)*major+j for j in range(1,major+1)])
        for j in range(major):
            col2[i-1+j*major] = change[j]
    for i in range(major*major):
        sample_space[i,0] = ((np.random.random()+col1[i]-1)/major**2)*2.75-2
        sample_space[i,1] = ((np.random.random()+col2[i]-1)/major**2)*2.5-1.25

    return sample_space