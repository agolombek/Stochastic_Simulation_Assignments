import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image, ImageDraw
from math import log, log2

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

#mandelbrot_plot(5000,1000,[-2,0.75],[-1.25,1.25],"full_fractal")
#mandelbrot_plot(5000,1000,[-0.57,-0.4],[-0.5,-0.625],"zoom1")

def mandelbrot_area(iterations,samples,re_axis,im_axis):

  re_ax_start = re_axis[0]
  re_ax_end = re_axis[1]
  im_ax_start = im_axis[0]
  im_ax_end = im_axis[1]
  counter = 0
  for i in range(1,samples):
    c = complex(np.random.uniform(re_ax_start,re_ax_end),np.random.uniform(im_ax_start,im_ax_end))
    m = mandelbrot(c,iterations)
    counter = counter + 1 if m == iterations else counter

  return counter/samples * (re_ax_end - re_ax_start) * (im_ax_end - im_ax_start)

"""Plot Area of Mandelbrot set"""

#print(mandelbrot_area(1000,1000000,[-2,0.75],[-1.25,1.25]))


    
