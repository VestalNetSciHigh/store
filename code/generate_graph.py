__author__ = 'VestalNetSciHigh'

# Generate a "Gephiable" graph from data

from numpy import loadtxt
import networkx as nx
import settings
import time

DATAFILE = "clipped_distances.dat"

start_time = time.time()
output_string = ""

# load output from parseCSV
distances = loadtxt(settings.OUTPUT+"\\"+DATAFILE)

# Create a networkx graph
G = nx.from_numpy_matrix(distances)
output_string += str(G.edges()) + "\n"
nx.write_graphml(G, settings.OUTPUT+"\\graph.graphml")

total_seconds = time.time() - start_time
output_string += "Finished 'generate_graph.py' in " + str(total_seconds) + " seconds!"
settings.output(output_string, "graph_generation", mode="write")
print "Finished 'generate_graph.py' in " + str(total_seconds) + " seconds!"