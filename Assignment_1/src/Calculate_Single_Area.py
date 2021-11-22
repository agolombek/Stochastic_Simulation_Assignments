# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 19:12:18 2021

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

start_time = time()
random_sample = random_sampling(int(300))
res_random, it_random = Mandelbrot_Area(100000,random_sample,1e-3)
print("random: ",res_random, it_random)
end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours') 


start_time = time()
latin = latin_hypercube_sampling(int(300))
res_latin, it_latin = Mandelbrot_Area(100000,latin,1e-3)
print("latin: ",res_latin, it_latin)
end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours') 

start_time = time()
ortho = orthogonal_sampling(int(300))
res_ortho, it_ortho = Mandelbrot_Area(100000,ortho,1e-3)
print("ortho: ",res_ortho, it_ortho)
end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours') 

start_time = time()
ortho2 = orthogonal_sampling_01(int(300))
res_opt, it_opt = Mandelbrot_Area_really_improved(100000,ortho2,1e-3)
print("opt: ",res_opt, it_opt)
end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours') 