import numpy as np
import matplotlib.pyplot as plt
import random


def mandelbrot(iterations,samples):
    
  '''
  This function takes two arguments, iterations and samples.
  Samples is the number of samples generated, iterations is the number of 
  iterations each sample is chekced for convergence.
  The function returns 4 arrays, the real and imaginary components of both
  the stable and unstable samples.
  ''' 
  
  # Array for the points in the Mandelbrot set
  stable_real = []
  stable_imag = []

  # Array for the points not in the Mandelbrot set
  not_stable_real = []
  not_stable_imag = []
  
  for i in range(samples): 

    # Generating c between -2 and 2
    real_c = random.uniform(-2, 0.75)
    imag_c = random.uniform(-1.25, 1.25)
    c = real_c + imag_c*1j

    # Initialise z
    z = 0

    for i in range(iterations+1):
        
        norm_squared = abs(z)
        if norm_squared > 4:
            not_stable_real.append(real_c)
            not_stable_imag.append(imag_c)
            break
        
        elif i == iterations:
            stable_real.append(real_c)
            stable_imag.append(imag_c)
            
        else:
            z = z**2+c
    

  return stable_real,stable_imag, not_stable_real, not_stable_imag


"""Plot Mandelbrot set"""

# stable_real, stable_imag, not_stable_real, not_stable_imag = mandelbrot(3000,1000000)

# plt.plot(stable_real,stable_imag,"k.")
# plt.plot(not_stable_real,not_stable_imag,"r.")
# plt.xlim(-2,0.75)
# plt.ylim(-1.25,1.25)
# plt.show()

"""Plot Area of Mandelbrot set"""

sample_space = np.logspace(2, 7, 6)
all_areas = []

for samples in sample_space:
    stable_real, stable_imag, not_stable_real, not_stable_imag = mandelbrot(2000,int(samples))
    area = (2.75*2.5)*len(stable_real)/(len(stable_real)+len(not_stable_real))
    all_areas.append(area)
    print(area)

plt.plot(sample_space, all_areas)
plt.xscale('log')
plt.show()
    
