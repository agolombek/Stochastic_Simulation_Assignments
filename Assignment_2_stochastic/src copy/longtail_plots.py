# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 12:23:37 2021

@author: arong
"""
"""
In the following file, there are the functions used to generate the plots for the MLn queuing system.
The plot change varying the variables in the "variables" section.
"""

import simpy
import random
import numpy as np
import time
import matplotlib.pyplot as plt
"""
customer takes as arguments the sympy environment, the numbers of customers, 
the value of lambda, the counter, and 2 empty arrays. With these arrays we compute the 
mean waiting time and the mean service time

"""

def customer(env, number, lamda_tot, counter, wait_times, serv_times):
    for i in range(number):
        c = service(env, counter, wait_times, serv_times)
        env.process(c)
        t = random.expovariate(lamda_tot)
        yield env.timeout(t)
    return wait_times, serv_times
        
"""
service takes as arguments the sympy environment, the counter,
the value of mu, and 2 empty arrays. With these arrays we compute the 
mean waiting time and the mean service time

""" 

def service(env, counter, wait_times, service_times):
    """Customer arrives, is served and leaves."""
    arrive = env.now
   
    with counter.request() as req:
        yield req

        wait = env.now - arrive
        wait_times.append(wait)
        
        service_start = env.now
        t = 0.75*random.expovariate(1) + 0.25*random.expovariate(0.2)
        yield env.timeout(t)
        service_time = env.now - service_start
        service_times.append(service_time)

############## VARIABLES for the plot ###############

n_range = [1, 2, 4]         # number of counters to be tested for
mu = 0.5                   # 5 minutes average service time
num_points = 25
customers = 10000           # customers per run
max_std = 1          
rho_range = np.linspace(0.5, 0.98, num_points)

####################################################

solution = np.zeros((num_points*len(n_range), 5))
i = 0

start = time.time()

for num_counters in n_range:
    for rho in rho_range:
        
        lamda_counter = rho*mu
        lamda_tot = lamda_counter*num_counters
        
        env = simpy.Environment()
        wait_times = []
        serv_times = []
        counter = simpy.Resource(env, num_counters)
        env.process(customer(env, customers, lamda_tot, counter, wait_times, serv_times))
        env.run()
        
        
        A = np.mean(wait_times)
        S = 0
        n = 0
        std = 1
        l = 1
        
        while std > max_std or l < 100:
            #preform bootstrapping
            env = simpy.Environment()
            wait_times = []
            serv_times = []
            counter = simpy.Resource(env, num_counters)
            env.process(customer(env, customers, lamda_tot, counter, wait_times, serv_times))
            env.run()
            # Update A and standrad deviation
            new_wait_avg = np.mean(wait_times)
            l += 1
            S = ((l-2)/(l-1))*S+(new_wait_avg-A)**2/l
            A = (new_wait_avg+(l-1)*A)/l
            n += 1
            std = 1.96*np.sqrt(S/(n))
            max_std = 0.01*A
            
        print(num_counters, rho, A, n, std) 
        
        solution[i, 0] = num_counters
        solution[i, 1] = rho
        solution[i, 2] = A
        solution[i, 3] = n
        solution[i, 4] = std
        
        i += 1



end = time.time()
print('The runtime was', (end-start)/(60*60), 'hours') 
        
############################# Plotting ####################################

start_idx = 0
idx = num_points
for i in range(len(n_range)):
    n = solution[:,0][start_idx:idx][0]
    rho = solution[:,1][start_idx:idx]
    mean_wait = solution[:,2][start_idx:idx]
    error_bars = 0.01*mean_wait
    
    start_idx += num_points
    idx += num_points
    
    plot_label = "M/L/" + str(int(n))
    plt.errorbar(rho, mean_wait, yerr=error_bars, capsize=5,label=plot_label)
    
plt.grid()
plt.legend()
plt.ylabel('mean wait [min]')
plt.xlabel('system load')
plt.show()

start_idx = 0
idx = num_points
for i in range(len(n_range)):
    n = solution[:,0][start_idx:idx][0]
    rho = solution[:,1][start_idx:idx]
    iterations = solution[:,3][start_idx:idx]
    
    start_idx += num_points
    idx += num_points
    
    plot_label = "M/L/" + str(int(n))
    plt.plot(rho, iterations, label=plot_label)
    
plt.grid()
plt.legend()
plt.ylabel('iterations')
plt.xlabel('system load')
plt.show()