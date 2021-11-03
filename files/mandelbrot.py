import numpy as np
import matplotlib.pyplot as plt
import random

def mandelbrot(iter,s): # iter is the number of iterations, s is the number of samples
  for i in range(s): 

    # Array for the points in the Mandelbrot set
    stable_real = []
    stable_imag = []

    # Array for the points not in the Mandelbrot set
    not_stable_real = []
    not_stable_imag = []

    # Generating c between -2 and 2
    real_c = random.random()*4 - 2
    imag_c = (random.random()*4 - 2)*1j
    c = real_c + imag_c

    # Initialise z
    z = 0

    for i in range(iter):
      norm_squared = z.real ** 2 + z.imag**2
      if norm_squared > 4:
        not_stable_real.append(real_c)
        not_stable_imag.append(imag_c)
        break
      else:
        z = z**2+c
    # Appending the c point in the stable set
    stable_real.append(real_c)
    stable_imag.append(imag_c)

  return stable_real,stable_imag

stable_real, stable_imag = mandelbrot(10,100)
print(stable_real, stable_imag)

plt.plot(stable_real,stable_imag,"ro")
plt.show()
    
c = 

