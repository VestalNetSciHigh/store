__author__ = 'VestalNetSciHigh'

import matplotlib.pyplot as plt
import networkx as nx
import settings
import time
import os

start_time = time.time()

# load graph.graphml
G = nx.read_graphml(open(settings.OUTPUT + "\\graph.graphml"))

# Generate graph types
GRAPH_TYPES = [["draw_spring", nx.spring_layout(G)],
               ["draw_spectral", nx.spectral_layout(G)],
               ["draw_circular", nx.circular_layout(G)]]

# draw
path = settings.OUTPUT+"\\graphs\\"
if not os.path.exists(path):
    os.makedirs(path)

print

for i in xrange(GRAPH_TYPES.__len__()):
    for node in GRAPH_TYPES[i][1]:
        x, y = GRAPH_TYPES[i][1][node]
        plt.text(x-0.05, y+0.05, s=nx.get_node_attributes(G, settings.NAME_STRING_KEY).pop(str(node)),\
                 bbox=dict(facecolor='red', alpha=0.4), horizontalalignment='center')
    nx.draw(G, GRAPH_TYPES[i][1])
    plt.savefig(path+GRAPH_TYPES[i][0])
    plt.clf()

total_seconds = time.time() - start_time
print "Finished 'draw_graph.py' in " + str(total_seconds) + " seconds!"