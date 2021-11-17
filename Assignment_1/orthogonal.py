import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2
from time import time
from numba import njit


@njit
def orthogonal(major):
	samples = major * major
	vec_x = np.zeros((samples))
	vec_y = np.zeros((samples))

	xlist = np.zeros((major,major))
	ylist = np.zeros((major,major))
	samples_size = major*major
	m = 0
	for i in range(major):

		for j in range(major):

			m += 1
			xlist[i][j] = ylist[i][j] = m

	for k in range(1):

		for i in range(major):
			xlist[i] = np.random.permutation(xlist[i])
			ylist[i] = np.random.permutation(ylist[i])

	for i in range(major):

		for j in range(major):
			scale = 1
			x = -2.0 + scale * xlist[i][j] + np.random.random()
			y = -2.0 + scale * ylist[i][j] + np.random.random()	
			vec_x[i*j] = x
			vec_y[i*j] = y
	return vec_x,vec_y

x,y = orthogonal(10)

for i in range(100):

	for j in range(100):

		plt.plot(x[i],y[j],"r.")

plt.show()

