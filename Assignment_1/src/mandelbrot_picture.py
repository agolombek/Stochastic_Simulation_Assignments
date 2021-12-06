import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2
from time import time


"""
in this file there are the function uset to make the pictures of the fractal

"""

def mandelbrot(c,iterations):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iterations:
        z = z*z + c
        n += 1

    if n == iterations:
        return iterations
    
    return n + 1 - log(log2(abs(z)))
    


def mandelbrot_plot(division,iterations,re_axis,im_axis,name):
  # Plot window
  re_ax_start = re_axis[0]
  re_ax_end = re_axis[1]
  im_ax_start = im_axis[0]
  im_ax_end = im_axis[1]

  im = Image.new('RGB', (division, division), (0, 0, 0))
  draw = ImageDraw.Draw(im)

  for x in range(0, division):
      for y in range(0, division):
          # Convert pixel coordinate to complex number
          c = complex(re_ax_start + (x / division) * (re_ax_end - re_ax_start),
                      im_ax_start + (y / division) * (im_ax_end - im_ax_start))
          # Compute the number of iterations
          m = mandelbrot(c,iterations)
          # The color depends on the number of iterations
          red = 52+int(log(log((m)))*255) if m < iterations else 0
          green = 179+int(log(log((m)))*100) if m < iterations else 0
          blue = 110+int(log(log((m)))*140) if m < iterations else 0
          # Plot the point
          draw.point([x, y], (red, green, blue))

  im.save(name, 'PNG')

"""
Uncomment the code below to show the fractals
"""
start_time = time() 

mandelbrot_plot(15000,1000,[-2,0.75],[-1.25,1.25],"full_fractal_high_res")
# mandelbrot_plot(5000,1000,[-0.57,-0.4],[-0.5,-0.625],"zoom1")


end_time = time()       
print('The runtime was', (end_time-start_time)/(60*60), 'hours') 
