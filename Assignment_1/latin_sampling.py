import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2
from time import time
from numba import njit

@njit
def latin(samples,sample_space):
	all_samples = np.zeros((int(samples)+1, 2))

	#defining the lenght of the cell along the x-axes
	dx = (sample_space[0][1]-sample_space[0][0])/(samples+1)

	#defining the lenght of the cell along the y-axes
	dy = (sample_space[1][1]-sample_space[1][0])/(samples+1)

	#printing the grid
	x = np.arange(sample_space[0][0],sample_space[0][1],dx)
	y = np.arange(sample_space[1][0],sample_space[1][1],dy)
	
	for i in range(0,len(y)):
		x_point = np.random.choice(x)
		x = np.delete(x, np.where(x == x_point))
		y_sample = np.random.uniform(y[i],y[i]+dy)
		x_sample = np.random.uniform(x_point,x_point+dx)
		all_samples[i, 0] = x_sample
		all_samples[i, 1] = y_sample
		
	return all_samples
	



start_time = time()
print(latin(10000.,[[0,1],[0,1]]))
end_time = time()

print(end_time-start_time)