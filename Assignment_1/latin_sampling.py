import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2
from time import time
from numba import njit


def latin(samples):

    # generating #samples number of points in the space
    samples_vector = []
    perm1 = np.random.permutation(samples)
    perm2 = np.random.permutation(samples)
    for i in range(samples):
        samples_vector.append([((np.random.uniform()+perm1[i])/samples)*2.75-0.75,((np.random.uniform()+perm2[i])/samples)*2.5-1.25])

    return samples_vector

@njit
def latin_numba(samples):

    # generating #samples number of points in the space
    samples_vector = np.zeros((samples, 2))
    perm1 = np.random.permutation(samples)
    perm2 = np.random.permutation(samples)
    for i in range(samples):
        samples_vector[i, 0] = ((np.random.random()+perm1[i])/samples)*2.75-0.75
        samples_vector[i, 1] = ((np.random.random()+perm2[i])/samples)*2.5-1.25
    return samples_vector



# start_time = time()
# all_samples = latin(1000)
# end_time = time()
# print(end_time - start_time)


# for i in np.linspace(-0.75,2,101):
#     for j in np.linspace(-1.25,1.25,101):
#         plt.plot(i,j,"b.")
# for point in all_samples:
#     plt.plot(point[0], point[1],"r.")

# plt.show()

start_time = time()
all_samples = latin_numba(50)
end_time = time()
print(end_time-start_time)


for i in np.linspace(-0.75,2,51):
    for j in np.linspace(-1.25,1.25,51):
        plt.plot(i,j,"b.")

for [x, y] in all_samples:
    plt.plot(x, y,"r.")

plt.show()

