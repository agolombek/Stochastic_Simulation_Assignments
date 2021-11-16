import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2
from time import time
from numba import njit


#@njit
#latin between 0 and 1
def latin(samples):

	# generating #samples number of points in the space
	samples_vector = []
	perm1 = np.random.permutation(samples)
	perm2 = np.random.permutation(samples)
	for i in range(samples):
		samples_vector.append([((np.random.uniform()+perm1[i])/samples)*2.75-0.75,((np.random.uniform()+perm2[i])/samples)*2.5-1.25])

	return samples_vector

def latin2(samples):

	# generating #samples number of points in the space
	samples_vector = []
	perm1 = np.random.permutation(samples)
	perm2 = np.random.permutation(samples)
	for i in range(samples):
		samples_vector.append([(np.random.uniform(-0.75, 2)+perm1[i]*2.75)/samples,(np.random.uniform(-1.25, 1.25)+perm2[i]*2.5)/samples])

	return samples_vector




start_time = time()

all_samples = latin(10)
print(all_samples)


end_time = time()

for i in np.linspace(-0.75,2,11):
	for j in np.linspace(-1.25,1.25,11):
		plt.plot(i,j,"b.")

for point in all_samples:
	plt.plot(point[0], point[1],"r.")

plt.show()