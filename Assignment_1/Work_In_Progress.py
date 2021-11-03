import numpy as np
import matplotlib.pyplot as plt
import random

def mandelbrot_area(iterations,samples): # iterations is the number of iterations, samples is the number of samples
  
  '''
  This function takes two arguments, iterations and samples.
  Samples is the number of samples generated, iterations is the number of 
  iterations each sample is chekced for convergence.
  The function returns the number of stable and unstable samples.
  ''' 
  
  stable = 0
  not_stable = 0
  
  for i in range(samples): 

    # Generating c in required range
    real_c = random.uniform(-2, 0.75)
    imag_c = random.uniform(-1.25, 1.25)
    c = real_c + imag_c*1j

    # Initialise z
    z = 0

    for i in range(iterations+1):
        
        norm_squared = abs(z)
        if norm_squared > 4:
            not_stable += 1
            break
        
        elif i == iterations:
            stable += 1
            
        else:
            z = z**2+c
    
  return stable, not_stable 


"""Plot Area of Mandelbrot set for increasing sample numbers"""

sample_space = np.logspace(2, 7, 6)
all_areas = []

for samples in sample_space:
    stable, not_stable = mandelbrot_area(2000,int(samples))
    area = (2.75*2.5)*stable/(stable + not_stable)
    all_areas.append(area)
    print(area)

plt.plot(sample_space, all_areas)
plt.xscale('log')
plt.show()



