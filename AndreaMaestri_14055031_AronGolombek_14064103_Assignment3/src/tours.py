import tsplib95

#----------------- pcb442 ---------------------
pcb442 = tsplib95.load('../TSP-Configurations/pcb442.tsp.txt')
pcb442_nodes = pcb442.as_name_dict()["node_coords"]

pcb442_sol = tsplib95.load('../TSP-Configurations/pcb442.opt.tour.txt')
pcb442_solved = pcb442_sol.as_name_dict()["tours"]
pcb442_solved = pcb442_solved[0]

pcb442_keyss =  list(pcb442_nodes.keys())

#----------------- a280 ---------------------
a280 = tsplib95.load('../TSP-Configurations/a280.tsp.txt')
a280_nodes = a280.as_name_dict()["node_coords"]

a280_sol = tsplib95.load('../TSP-Configurations/a280.opt.tour.txt')
a280_solved = a280_sol.as_name_dict()["tours"]
a280_solved = a280_solved[0]


a280_keyss =  list(a280_nodes.keys())

#----------------- eil51 ---------------------

eil51 = tsplib95.load('../TSP-Configurations/eil51.tsp.txt')
eil51_nodes = eil51.as_name_dict()["node_coords"]

eil51_sol = tsplib95.load('../TSP-Configurations/eil51.opt.tour.txt')
eil51_solved = eil51_sol.as_name_dict()["tours"]
eil51_solved = eil51_solved[0]


eil51_keyss =  list(eil51_nodes.keys())