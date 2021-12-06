# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 12:14:31 2021

@author: arong
"""

# Movie Theater Simluation
# Goal - Average Wait - 10 minutes or less

import simpy
import random
import statistics

wait_times = []


class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 6))

def go_to_movies(env, moviegoer, theater):
    # arrives at theater
    arrival_time = env.now

    # buy ticket
    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))
    
    # check ticket
    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))
    
    # buy food
    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))

    # go to their seat
    wait_times.append(env.now - arrival_time)

def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    for moviegoer in range(3):
        env.process(go_to_movies(env, moviegoer, theater))
    
    while True:
        yield env.timeout(0.20)

        moviegoer += 1
        env.process(go_to_movies(env, moviegoer, theater))
    
def calculate_wait_times(wait_times):
    average_wait = statistics.mean(wait_times)
    # pretty print results:
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def main(num_cashiers, num_servers, num_ushers):
    # Setup
    random.seed(42)

    # Run the simulation
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)

    # View the results
    mins, secs = calculate_wait_times(wait_times)
    print(
        "Running simulation...",
        f"\nThe average wait time is {mins} minutes and {secs} seconds.",
    )
    
    
main(5, 4, 4)

