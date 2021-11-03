import numpy as np
import matplotlib.pyplot as plt
import random

def mandelbrot_plot(iterations,samples):
    """
    function returns a plot of the mandelbrot set.
    iterations is the number of iterations each sample is checked for and
    samples is the number of samples taken.
    """
    for i in range(samples): 
        
        # Generating c between -2 and 2
        real_c = random.random()*4 - 2
        imag_c = random.random()*4 - 2
        c = real_c + imag_c*1j
    
        # Initialise z
        z = 0
    
        for i in range(iterations):
          norm_squared = abs(z)
          if norm_squared > 4:
              plt.plot(real_c, imag_c, marker='.', color='black')
              break
          else:
            z = z**2+c
        # Appending the c point in the stable set
        plt.plot(real_c, imag_c, marker='.', color='red')
    plt.ylim(-2,2)
    plt.xlim(-2,2)
    plt.show
    
mandelbrot_plot(100, 10000)



