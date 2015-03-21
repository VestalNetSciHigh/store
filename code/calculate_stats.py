__author__ = 'VestalNetSciHigh'

""" Read in data (and array of distance metrics) and calculate various stats """

import time
# from numpy import loadtxt
import numpy
import settings
import datetime

start_time = time.time()
print "Started: " + datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
output_string = ""

# load output from parseCSV
distances = numpy.loadtxt(settings.OUTPUT+"\\real_distances.dat")

# sort all distances
ordered_distances = []
for i in xrange(distances.__len__()):
    for id in distances[i]:
        ordered_distances.append(id)
ordered_distances.sort()
output_string += "Total distances: " + str(ordered_distances.__len__()) + "\n"

# compute mean distance
mean_distance = sum(ordered_distances) / ordered_distances.__len__()
output_string += "Mean distance: " + str(mean_distance) + "\n"
settings.output(str(mean_distance), "mean_distance", ext=".dat", mode="write")

# compute root mean square
sum_squares = 0
for dist in ordered_distances:
    sum_squares += dist * dist
root_mean_square = pow(sum_squares / float(ordered_distances.__len__()), 0.5)
output_string += "Root mean square: " + str(root_mean_square) + "\n"

# minimum distance (most dissimilar)
most_dissimilar = ordered_distances[0]
output_string += "Most dissimilar (min): " + str(most_dissimilar) + "\n"
settings.output(str(most_dissimilar), "most_dissimilar", ext=".dat", mode="write")

# compute median distance
median_distance = 0
index_float = ordered_distances.__len__() / 2.0
index_whole = ordered_distances.__len__() / 2  # intentional truncation
if index_float - index_whole < 0.001:
    median_distance = (ordered_distances[index_whole] + ordered_distances[index_whole + 1]) / 2.0
else:
    median_distance = ordered_distances[index_whole]
output_string += "Median distance: " + str(median_distance) + "\n"

# other stats
std = numpy.std(ordered_distances)
settings.output(str(std), "standard_deviation", ext=".dat", mode="write")

var = numpy.var(ordered_distances)
output_string += "Stardard Dev.: " + str(std)
output_string += "Variance: " + str(var)

total_seconds = time.time() - start_time
output_string += "Finished 'calculate_stats.py' in " + str(total_seconds) + " seconds!"
settings.output(output_string, "stats_real_valued", mode="write")
print "Finished 'calculate_stats.py' in " + str(total_seconds) + " seconds!"