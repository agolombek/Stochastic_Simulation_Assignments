# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 10:57:03 2021

@author: arong
"""

import simpy
import random
import statistics
import numpy.random as rnd

wait_times = []
service_times = []


class Service_Queue(object):
    def __init__(self, env, num_servers):
        self.env = env
        self.server = simpy.Resource(env, num_servers)

    def perform_service(self, moviegoer):
        yield self.env.timeout(rnd.exponential(scale=1))


def customer_wait(env, customer, service_queue):
    # arrives at theater
    arrival_time = env.now

    # buy ticket
    with service_queue.server.request() as request:
        yield request
        yield env.process(service_queue.perform_service(customer))
    
    # go to their seat
    wait_times.append(env.now - arrival_time)

def run_service(env, num_servers):
    service_queue = Service_Queue(env, num_servers)
    
    customer = 0

    while True:
        service_start = env.now
        yield env.timeout(rnd.exponential(scale=1.2))
        
        customer += 1
        env.process(customer_wait(env, customer, service_queue))

        service_times.append(env.now - service_start)

    
def calculate_wait_times(wait_times):
    average_wait = statistics.mean(wait_times)
    # pretty print results:
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def calculate_service_times(service_times):
    average_serv = statistics.mean(service_times)
    # pretty print results:
    minutes, frac_minutes = divmod(average_serv, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def main(num_servers):
    # Setup
    # rnd.seed(42)

    # Run the simulation
    env = simpy.Environment()
    env.process(run_service(env, num_servers))
    env.run(until=120)

    # View the results
    mins_wait, secs_wait = calculate_wait_times(wait_times)
    mins_serv, secs_serv = calculate_service_times(service_times)
    print('average wait = ', mins_wait,' minutes and ', secs_wait, ' seconds')
    print('average service = ', mins_serv,' minutes and ', secs_serv, ' seconds')
    
main(1)
    
    
        
        
