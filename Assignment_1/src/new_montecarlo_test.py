import numpy as np
import random
from numba import njit
from time import time
import matplotlib.pyplot as plt

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
            z = z*z + complex(c[0]*2.75-2, c[1]*2.5-1.25)
            n += 1

        if n == iterations:
            answer[i] = 1
  
        i += 1
    return answer



@njit
def mandelbrot_improved(points, iterations, size):
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
    answer = np.zeros((size))
    i = 0
    for c in points:
        c_val = complex(c[0]*2.75-2, c[1]*1.25)
        z = c_val + c_val*c_val
        n = 0
        while abs(z) <= 2 and n < iterations and abs(z - c_val)>0.000001:
            z = z*z + c_val
            n += 1

        if n == iterations or abs(z - c_val)<0.000001:
            answer[i] = 1
        
        i += 1
    return answer

@njit
def Mandelbrot_Area(iterations, sample, max_std):

    points = mandelbrot(sample, iterations, int(sample.size/2))
    A = np.mean(points)*(2.75*2.5)
    print(A)
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
def Mandelbrot_Area_improved(iterations, sample, max_std):

    points = mandelbrot_improved(sample, iterations, int(sample.size/2))
    A = np.mean(points)*(2.75*1.25)
    print(A)
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

    return A, n




    
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
        sample_space[i, 0] = np.random.uniform(0,1)
        sample_space[i, 1] = np.random.uniform(0,1)
    return sample_space


sample = random_sampling(1000)

start1 = time()
res,it = Mandelbrot_Area_improved(100000,sample,1e-3)
fin1 = time()
print("Area improved:",res*2,"    number of iterations improved: ",it,"    time improved:",fin1-start1)

sample2 = random_sampling(int(np.sqrt(2000000)))
start2 = time()
res2,it2= Mandelbrot_Area(100000,sample2,1e-3)
fin2 = time()
print("Area:",res2,"    number of iterations: ",it2,"    time: ",fin2-start2)


