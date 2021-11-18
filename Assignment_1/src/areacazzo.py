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

@njit
def Mandelbrot_Area_2(x_values, samples, max_std):
    """
    This functions estimates the area of the mandelbrot set over a grid of 
    varying iterations and sample sizes, given a ceratin sampling function.
    --------------------------------------------------------------------------
    The argument x_values is an array containing all the numbers of iterations 
    each point in the sample space is tested for divergence.
    
    The argument y_values represents all the sampling for different values of S.
    Together with x_values it forms the grid over which all values for which the 
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
        for sample in samples:
            samp = int(sample.size/2)
            # test all the points in the sample x times for convergence
            # generating the sample using the sampling function
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
            while std > max_std or l < 10:
                
                #preform bootstrapping
                counter = 0
                for i in range(int(samp)):
                    counter += np.random.choice(points)
                    
                area_bootstrapping = (2.75*2.5)*counter/samp
                # Update Area and standrad deviation
                print(l)
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



start_time = time() 
x_values = np.logspace(2, 5, 3) 
sample_range_sqrt = np.array([100,200,300])
sample_range = np.array([100,200,300])

ortho = sampling_numba(sample_range_sqrt,orthogonal_sampling)
print(ortho)

# latin = sampling(sample_range,latin_hypercube_sampling)
# random = sampling(sample_range,random_sampling)
        
# answer = Mandelbrot_Area_2(x_values, ortho, 1e-2)

# iterations = answer[:,0]
# samples = answer[:,1]
# area = answer[:,2]
# bootstrap_it = answer[:,3]
         
# end_time = time()

# print('The runtime was', (end_time-start_time)/(60*60), 'hours')   

# ############################# 3D PLOTTING ###################################

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# ax.plot_trisurf(np.log10(iterations),np.log10(samples), np.absolute(area-1.506484), linewidth=0, antialiased=True,cmap=cm.jet)
# ax.xaxis.set_major_locator(MaxNLocator(5))
# ax.yaxis.set_major_locator(MaxNLocator(6))
# ax.zaxis.set_major_locator(MaxNLocator(5))
# ax.tick_params(labelsize=16)
# ax.set_xlabel(r'$Iterations$ ', fontsize=20, rotation=150)
# ax.set_ylabel(r'$Samples$', fontsize=20)
# ax.set_zlabel(r'$|A_{i,s} - A_M|$', fontsize=20, rotation=60)
# plt.show()