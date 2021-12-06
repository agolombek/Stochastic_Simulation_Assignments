import simpy
import random
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
"""
In the following file, there are the functions used to generate the plots for the MDn queuing system.
The plot change varying the variables in the "variables" section.
"""

"""
customer takes as arguments the sympy environment, the numbers of customers, 
the value of lambda, the counter, and 2 empty arrays. With these arrays we compute the 
mean waiting time and the mean service time

"""
def customer(env, number, lamda_tot, counter, wait_times, serv_times):
    for i in range(number):
        c = service(env, counter, mu, wait_times, serv_times)
        env.process(c)
        t = random.expovariate(lamda_tot)
        yield env.timeout(t)
    return wait_times, serv_times
"""
service takes as arguments the sympy environment, the counter,
the value of mu, and 2 empty arrays. With these arrays we compute the 
mean waiting time and the mean service time

"""         
def service(env, counter, mu, wait_times, service_times):
    """Customer arrives, is served and leaves."""
    arrive = env.now
   
    with counter.request() as req:
        yield req

        wait = env.now - arrive
        wait_times.append(wait)
        
        service_start = env.now
        t = random.expovariate(mu)
        yield env.timeout(t)
        service_time = env.now - service_start
        service_times.append(service_time)

############## VARIABLES for the plot ###############

simulations = 500        			# number of customers to be tested for 
mu = 1/5                    		# 5 minutes average service time
customers = [100,1000,10000]        # customers per run
rho_values = [0.5,0.74,0.98]

#####################################################

for rho in rho_values:
	l = -1
	for n in range(len(customers)):
		l = l+1
		color = ["gold", "seagreen", "deepskyblue"]
		waiting_vector = []
		lamda = rho*mu
		for i in range(simulations):
			env = simpy.Environment()
			wait_times = []
			serv_times = []
			counter = simpy.Resource(env, 1)
			env.process(customer(env, customers[n], lamda, counter, wait_times, serv_times))
			env.run()
			waiting_vector.append(np.mean(wait_times))

		
		sns.histplot(waiting_vector,kde = True, bins = 20, stat = "density",color = color[l],label = f"k ={customers[n]}")
	plt.legend()
	plt.grid()
	plt.title(f"system load = {rho}")
	plt.xlabel("Mean waiting time")
	plt.show()