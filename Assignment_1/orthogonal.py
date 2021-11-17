import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2
from time import time
from numba import njit


@njit
def orthogonal_array(major):
	array1 = np.zeros((major*major))
	array2 = np.zeros((major*major))

	# changing the elements of the second column
	for j in range(major):
		for i in range(major):
			array2[i+major*j]=i+1

	return array1, array2


def orthogonal_sampling(major):
	
	samples_vector = np.zeros((major*major,2))
	col1 = np.array([])
	col2 = np.zeros((major*major))
	#col1,col2 = orthogonal_array(major)
	# devo cambiare gli elementi a gruppi di #major
	for i in range(1,major+1):
		col1 = np.append(col1,np.random.permutation([(i-1)*major+j for j in range(1,major+1)]))

	# changing the elements of the second column
	for j in range(major):
		for i in range(major):
			col2[i+major*j]=i+1
	for i in range(1,major+1):
		change = np.random.permutation([(i-1)*major+j for j in range(1,major+1)])
		for j in range(major):
			col2[i-1+j*major] = change[j]
	for i in range(major*major):
		samples_vector[i,0] = ((np.random.random()+col1[i]-1)/major**2)*2.75-2
		samples_vector[i,1] = ((np.random.random()+col2[i]-1)/major**2)*2.5-1.25

	return samples_vector

		
all_samples = orthogonal_sampling(8)

for i in np.linspace(-2,0.75,9):
    for j in np.linspace(-1.25,1.25,9):
        plt.plot(i,j,"b.")
for point in all_samples:
    plt.plot(point[0], point[1],"r.")

plt.show()






