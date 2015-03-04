__author__ = 'VestalNetSciHigh'

# Output a .graphml file from data

from numpy import loadtxt
import networkx as nx
import settings
import time
import csv

DATATYPE = "clipped"  # May use: "clipped" | "real", referring to whether or not a threshold was used

start_time = time.time()
output_string = ""

# load output from parseCSV
distances = loadtxt(settings.OUTPUT+"\\"+DATATYPE+"_distances.dat")
csv_reader = csv.DictReader(open(settings.OUTPUT + "\\dict_data_selective_attributes.dat", "U"))

# Create a networkx graph
G = nx.from_numpy_matrix(distances)

# Add node data tags / attributes
fieldnames = csv_reader.fieldnames
for row in csv_reader:
    if row == "":
        pass
    for tag in fieldnames[1:]:
        G.node[int(row[fieldnames[0]])][tag] = row[tag]
print G.nodes(data=True)

# Add edge data, change color of edges above the average weight

output_string += str(G.edges()) + "\n"
nx.write_graphml(G, settings.OUTPUT+"\\graph.graphml")

total_seconds = time.time() - start_time
output_string += "Finished 'write_graph.py' in " + str(total_seconds) + " seconds!"
settings.output(output_string, "graph_generation", mode="write")
print "Finished 'write_graph.py' in " + str(total_seconds) + " seconds!"