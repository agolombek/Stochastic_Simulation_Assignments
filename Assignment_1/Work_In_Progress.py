import numpy as np
import matplotlib.pyplot as plt
import random

def mandelbrot(iter,s): # iter is the number of iterations, s is the number of samples
  # Array for the points in the Mandelbrot set
  stable_real = []
  stable_imag = []

  # Array for the points not in the Mandelbrot set
  not_stable_real = []
  not_stable_imag = []
  
  for i in range(s): 

    # Generating c between -2 and 2
    real_c = random.random()*6 - 3
    imag_c = (random.random()*6 - 3)
    c = real_c + imag_c*1j

    # Initialise z
    z = 0

    for i in range(iter):
      norm_squared = abs(z)
      if norm_squared > 4:
        not_stable_real.append(real_c)
        not_stable_imag.append(imag_c)
        break
      else:
        z = z**2+c
    # Appending the c point in the stable set
    stable_real.append(real_c)
    stable_imag.append(imag_c)

  return stable_real,stable_imag, not_stable_real, not_stable_imag

stable_real, stable_imag, not_stable_real, not_stable_imag = mandelbrot(10000,100000)

plt.plot(stable_real,stable_imag,"k.")
plt.plot(not_stable_real,not_stable_imag,"r.")
plt.ylim(-4,4)
plt.xlim(-4,4)
plt.show()