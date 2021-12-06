# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 10:12:49 2021

@author: arong
"""

import numpy as np

"""Variables for Welch Test"""

# x_bar = 
# std_x = 
# nx = 
# Sx = 

# y_bar = 
# std_y = 
# ny = 
# Sy = 

"""Variables for T Test"""

expectation = 171.49999999999983

x_bar = 61.66718774905547
std_x = 0.04384566681227879
nx = 11961
Sx = np.sqrt(nx)*std_x/1.96


def Welch_Actual_Value(x_bar, y_bar, Sx, Sy, nx, ny):
    return (x_bar-y_bar)/np.sqrt((Sx**2/nx)+(Sy**2/ny))

def dof(x_bar, y_bar, Sx, Sy, nx, ny):
    term_1 =(Sx**2/nx+Sy**2/ny)**2
    term_2 = Sx**4/(nx**2*(nx-1))
    term_3 = Sy**4/(ny**2*(ny-1))
    dof = term_1/(term_2+term_3)
    return dof

def Ttest_Actual_Value(expectation, x_bar, Sx, nx):
    return (x_bar-expectation)/(Sx/np.sqrt(nx))


"""Preform T Test"""
actual = np.abs(Ttest_Actual_Value(expectation, x_bar, Sx, nx))
critical= 1.96

print('Actual Value = ', actual)
print('Critical Value = ', critical)

if actual < critical:
    print('accept')
else:
    print('reject')












