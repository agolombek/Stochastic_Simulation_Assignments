import numpy as np 
import matplotlib.pyplot as plt
from tours import *
from tsp_functions import *
from time import time

start = time()

starting_keys = a280_keyss
nodes = a280_nodes
solved = a280_solved

num_simulations = 30
simulations_coordinates = []
length_values = []
all_length = []
solv = [nodes[solved[i]] for i in range(len(starting_keys))]
length2 = cost(solved,nodes)

for i in range(num_simulations):
	print(f"simulation number: {i+1}")
	
	# shuffling the keys, this is the initial solution
	keys = list(np.random.permutation(starting_keys))

	# initialising the i_th simulation
	chain = sim_annelling_adaptive_mutation([keys],4500,np.sqrt(len(keys))*5,nodes, mutation_2opt,mutation_insert,240,300)

	#chain = sim_annelling([keys],6000,np.sqrt(len(keys))*70,nodes, mutation_2opt,300)
	#chain = sim_annelling_cooling2([keys],4500,np.sqrt(len(keys))*5,nodes, mutation_2opt,300)

	# Saving the coordinates of the last configuration
	final_coordinates = [nodes[chain[-1][i]] for i in range(len(keys))]
	simulations_coordinates.append(final_coordinates)

	# Saving all the lenghts of a simulation (is this a good idea?)
	length = [cost(element,nodes) for element in chain]

	#all_length.append(length)

	# Saving the last value of the length 
	length_values.append(length[-1])

# finding the minimum value and the associated index

val, idx = min((val, idx) for (idx, val) in enumerate(length_values))
val_max, idx_max = max((val, idx) for (idx, val) in enumerate(length_values))

mean_value = np.mean(length_values)
std_value = np.std(length_values)

best_coordinates = simulations_coordinates[idx]
#best_lengths = all_length[idx]

# Confidence interval of the sample 
m, m_low, m_high = mean_confidence_interval(length_values)

end = time()

print(end-start)

print(f"best lenght : {val}")
print(f"worst length : {val_max}")
print(f"real lenght: {length2}")
print(f"length = {mean_value} +- {std_value}")
print(f"confidence interval: mean({m}), will lie in the interval [{m_low},{m_high}] with a probability of 95%")





# ---------------- Plotting ----------------

fig = plt.figure(figsize = (10,5))
st = fig.suptitle("TSP a280", fontsize="x-large")
ax1 = fig.add_subplot(121)
ax1.set_title("Benchmark solution")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax2 = fig.add_subplot(122)
ax2.set_title("Algorithm's Best Solution")
ax2.set_xlabel("x")
ax2.set_ylabel("y")

for first, second in zip(solv[:-1], solv[1:]):
	ax1.plot([first[0],second[0]],[first[1],second[1]],"b")
ax1.plot([solv[0][0],solv[-1][0]],[solv[0][1],solv[-1][1]],"b")
for coord in solv:
	ax1.plot(coord[0], coord[1], "ro", markersize=4)

for first, second in zip(best_coordinates[:-1], best_coordinates[1:]):
	ax2.plot([first[0],second[0]],[first[1],second[1]],"b")
ax2.plot([best_coordinates[0][0],best_coordinates[-1][0]],[best_coordinates[0][1],best_coordinates[-1][1]],"b")
for coord in best_coordinates:
	ax2.plot(coord[0], coord[1], "ro", markersize=4)

fig.tight_layout()

# shift subplots down:
st.set_y(0.95)
fig.subplots_adjust(top=0.85)

#------------------------------------

# remove tick marks
ax1.xaxis.set_tick_params(size=0)
ax1.yaxis.set_tick_params(size=0)

# change the color of the top and right spines to opaque gray
ax1.spines['right'].set_color((.8,.8,.8))
ax1.spines['top'].set_color((.8,.8,.8))

# tweak the axis labels
xlab = ax1.xaxis.get_label()
ylab = ax1.yaxis.get_label()

# remove tick marks
ax2.xaxis.set_tick_params(size=0)
ax2.yaxis.set_tick_params(size=0)

# change the color of the top and right spines to opaque gray
ax2.spines['right'].set_color((.8,.8,.8))
ax2.spines['top'].set_color((.8,.8,.8))

# tweak the axis labels
xlab = ax2.xaxis.get_label()
ylab = ax2.yaxis.get_label()

xlab.set_style('italic')
xlab.set_size(10)
ylab.set_style('italic')
ylab.set_size(10)

st.set_weight('bold')
#------------------------
plt.show()


fig = plt.figure(figsize=[7,5])
ax = plt.subplot(111)
l = ax.fill_between([i for i in range(len(length))],length)
# change the fill into a blueish color with opacity .3
l.set_facecolors([[.5,.5,.8,.1]])

# change the edge color (bluish and transparentish) and thickness
l.set_edgecolors([[0, 0, .5, .6]])
l.set_linewidths([1])

# remove tick marks
ax.xaxis.set_tick_params(size=0)
ax.yaxis.set_tick_params(size=0)

# change the color of the top and right spines to opaque gray
ax.spines['right'].set_color((.8,.8,.8))
ax.spines['top'].set_color((.8,.8,.8))

# tweak the axis labels
xlab = ax.xaxis.get_label()
ylab = ax.yaxis.get_label()

xlab.set_style('italic')
xlab.set_size(10)
ylab.set_style('italic')
ylab.set_size(10)

# tweak the title
ttl = ax.title
ttl.set_weight('bold')
plt.grid()
plt.xlabel("iterations")
plt.ylabel("path length")
plt.show()













