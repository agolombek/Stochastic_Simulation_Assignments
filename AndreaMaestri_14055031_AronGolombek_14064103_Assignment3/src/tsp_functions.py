import numpy as np 
import random
import scipy.stats

# Defining a function that computes the distance between 2 nodes
def distance ( node1, node2 ):
	return ((node1[0]-node2[0])**2 + (node1[1]-node2[1])**2)**0.5

'''
defining the cost function (i.e. given an array of nodes, computes the lenght of the road from 
the first to the last (and then back to the first)). We want that this function takes as an 
argument a list of keys, because we can shuffle that list without losing track of the cordinates of each node
'''
def cost(keys,nodes):
	cost = 0
	for i in range(len(keys)):
		if i != len(keys)-1:
			cost += round(distance(nodes[keys[i]],nodes[keys[i+1]]))
		else: 
			cost += round(distance(nodes[keys[i]],nodes[keys[0]]))
	return cost

# Defining the acceptance probability 
def accept(current, new_sol, T, nodes ):
	# Cost difference
	dC = cost(new_sol,nodes) - cost(current,nodes)

	if dC < 0:
		return new_sol
	else:
		# Fitness difference
		dF = np.exp(-dC/T)

		A = min(1,dF)
		

		# Condition
		if A == 1:
			return new_sol

		else: 
			U = random.random()
			if A >= U:
				return new_sol
			else:
				return current

# --------------- MUTATIONS -------------------
# 2-opt mutation
def mutation_2opt(current):

	# 2-opt algorithm
	new_sol = current[:]
	# Mutation of the copy
	l = random.randint(2, len(current) - 1)
	i = random.randint(0, len(current) - l)
	new_sol[i : (i + l)] = np.flipud(new_sol[i : (i + l)])
	
	return new_sol

# Swap between two nodes
def mutation_swap(current):

	# Swap algorithm
	new_sol = np.array(current[:])
	# Mutation of the copy
	l = random.randint(0, len(current) - 1)
	i = random.randint(0, len(current) - 1)
	new_sol[[i,l]] = new_sol[[l,i]]

	
	return list(new_sol)

# One node randomly moved into another position
def mutation_insert(current):

	# Mutation algorithm
	new_sol = current[:]
	# Mutation of the copy, the element in position l is insertd in position i
	l = random.randint(0, len(current) - 1)
	i = random.randint(0, len(current) - 1)
	v = new_sol[l]
	new_sol = np.delete(new_sol,l)
	new_sol = np.insert(new_sol, i, v)
	
	return list(new_sol)

# ----------- Metropolis algorithms and simulated annealing -------------

# Metropolis algorithm with a fixed temperature
def metropolis(chain, markov_lenght, T,nodes,mutation):

	acc_prob = 0

	for counter in range(markov_lenght):
		new_sol = mutation(chain[-1])
		new_current = accept(chain[-1],new_sol,T,nodes)
		# if new_sol == new_current:
		# 	acc_prob += 1
		chain.append(new_current)
		
	#print(acc_prob/markov_lenght)
	return chain

# Metropolis algorithm that takes track of the std in the chain 
def metropolis2(chain, markov_lenght, T,nodes,mutation):

	# acc_prob = 0
	std_vec = []

	for counter in range(markov_lenght):
		new_sol = mutation(chain[-1])
		new_current = accept(chain[-1],new_sol,T,nodes)
		std_vec.append(cost(new_current, nodes))
		# if new_sol == new_current:
		# 	acc_prob += 1
		chain.append(new_current)
		
	#print(acc_prob/markov_lenght)
	return [np.std(std_vec), chain]

# Simulated Annealing : metropolist step followed by a decrease in the temperature 
# This is for the cooling schedule 1
def sim_annelling(chain, markov_lenght, T,nodes,mutation,iterations):

	for counter in range(iterations):
		chain = metropolis(chain,markov_lenght,T,nodes,mutation)
		T *= 0.975
		print(counter+1)
		# print(T)

	return chain

# Simulated Annealing : metropolist step followed by a decrease in the temperature 
# This is for the cooling schedule 2
def sim_annelling_cooling2(chain, markov_lenght, T,nodes,mutation,iterations):

	for counter in range(iterations):
		params = metropolis2(chain,markov_lenght,T,nodes,mutation)
		chain = params[1]
		sigma = params[0]
		if sigma != 0:
			T *= (1+T/(3*sigma))**-1
		print(counter+1)
		# print(T)

	return chain

# This is for the adaptive mutation and cooling schedule 1
def sim_annelling_adaptive_mutation(chain, markov_lenght, T,nodes,mutation1,mutation2,iterations1,iterations2):
	
	for counter in range(iterations1):
		chain = metropolis(chain,markov_lenght,T,nodes,mutation1)
		T *= 0.975
		print(counter+1)

	for counter in range(iterations1,iterations2):
		chain = metropolis(chain,markov_lenght,T,nodes,mutation2)
		T *= 0.975
		print(counter+1)

	return chain

# Confidence interval
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

# Degrees of freedom for the welch test
def degrees_freedom(std1,std2,N1,N2):
	return ((std1**2/N1+std2**2/N2)**2)/(std1**4/((N1-1)*N1**2)+std2**4/((N2-1)*N2**2))

#print(degrees_freedom(52.96,39.95,40,40))