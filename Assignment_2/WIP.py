# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 11:02:55 2021

@author: arong
"""

import simpy
import random
import numpy as np


wait_times = []
service_times = []
inter_arrival_times = []

def customer(env, number, arrival_interval, counter):
    for i in range(number):
        c = service(env, counter)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)
        
def service(env, counter):
    """Customer arrives, is served and leaves."""
    arrive = env.now
   
    with counter.request() as req:
        yield req

        wait = env.now - arrive
        wait_times.append(wait)
        
        service_start = env.now
        t = random.expovariate(1.0 / mean_service_time)
        yield env.timeout(t)
        service_time = env.now - service_start
        service_times.append(service_time)


n = 3
customers = 10000
arrival_interval = 3
mean_service_time = 2

random.seed(42)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, n)
env.process(customer(env, customers, interval, counter))
env.run()

print('mean service time = ', np.mean(service_times))
print('mean wait = ', np.mean(wait_times))



    
