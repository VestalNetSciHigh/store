__author__ = 'VestalNetSciHigh'

# Output a .graphml file from data

from numpy import loadtxt
import networkx as nx
import settings
import time
import csv
import datetime

DATATYPE = "clipped"  # May use: "clipped" | "real", referring to whether or not a threshold was used

start_time = time.time()
print "Started: " + datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
output_string = ""

# load output from parseCSV
distances = loadtxt(settings.OUTPUT+"\\"+DATATYPE+"_distances+SD"+str(settings.NUM_STANDARD_DEVIATIONS)+".dat")
csv_reader = csv.DictReader(open(settings.OUTPUT + "\\dict_data_selective_attributes.dat", "U"))

# Create a networkx graph
G = nx.from_numpy_matrix(distances)

# Add node data tags / attributes
fieldnames = csv_reader.fieldnames
counter = 0
for row in csv_reader:
    if row == "":
        pass
    for index in xrange(settings.ATTRIBUTE_STRING_KEYS.__len__()):
        G.node[counter][settings.ATTRIBUTE_STRING_KEYS[index][1]] = row[settings.ATTRIBUTE_STRING_KEYS[index][0]]
    counter += 1

# Add edge data, change color of edges above the average weight

# output_string += str(G.edges()) + "\n"
nx.write_graphml(G, settings.OUTPUT+"\\graph"+settings.TARGET[12:] + "+SD" + str(settings.NUM_STANDARD_DEVIATIONS)+".graphml")


total_seconds = time.time() - start_time
print "Finished 'write_graph.py' in " + str(total_seconds) + " seconds!"