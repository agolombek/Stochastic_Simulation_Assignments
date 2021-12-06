# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 10:12:49 2021

@author: arong
"""

import numpy as np


x_bar = 30.264510302188565
std_x = 0.01*x_bar
nx = 12477
Sx = np.sqrt(nx)*std_x/1.96

y_bar = 107.62904204908953
std_y = 0.01*y_bar
ny = 10808
Sy = np.sqrt(ny)*std_y/1.96

critical_value = 1.96

def Actual_Value(x_bar, y_bar, Sx, Sy, nx, ny):
    return (x_bar-y_bar)/np.sqrt((Sx**2/nx)+(Sy**2/ny))

def dof(x_bar, y_bar, Sx, Sy, nx, ny):
    term_1 =(Sx**2/nx+Sy**2/ny)**2
    term_2 = Sx**4/(nx**2*(nx-1))
    term_3 = Sy**4/(ny**2*(ny-1))
    dof = term_1/(term_2+term_3)
    return dof

def MD1(rho,mu):

    return rho/((1-rho)*2*mu)

def ML1(rho, mu1, mu2):

    num = 0.75/mu1**2 + 0.25/mu2**2
    den = 0.75/mu1 + 0.25/mu2

    return num/den*(rho/(1-rho))

for i in [0.5,0.74,0.98]:
    print(f"MD1, rho = {i}: ",MD1(i,1/5))
    print(f"ML1, rho = {i}: ",ML1(i,1,0.2))

# print(dof(x_bar, y_bar, Sx, Sy, nx, ny))
# print(Actual_Value(x_bar, y_bar, Sx, Sy, nx, ny))

