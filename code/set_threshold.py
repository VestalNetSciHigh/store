__author__ = 'VestalNetSciHigh'

"""
Set all distances below a threshold to 0
Then, may also set non-zero distances to 1
SEE Configurable Constants below
"""

import time
from numpy import loadtxt
import os
import settings
import datetime

start_time = time.time()
print "Started: " + datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
output_string = ""

# load output from parseCSV.py
distances = loadtxt(settings.OUTPUT+"\\real_distances.dat")

# load output from calculate_stats.py (if exists)
most_dissimilar = 0
if os.path.exists(settings.OUTPUT+"\\"+"most_dissimilar.dat"):
    most_dissimilar = loadtxt(settings.OUTPUT+"\\most_dissimilar.dat")

average = 0
if os.path.exists(settings.OUTPUT+"\\"+"mean_distance.dat"):
    average = loadtxt(settings.OUTPUT+"\\mean_distance.dat")

standard_deviation = 0
if os.path.exists(settings.OUTPUT+"\\"+"standard_deviation.dat"):
    standard_deviation = loadtxt(settings.OUTPUT+"\\standard_deviation.dat")

threshold = average - (standard_deviation * settings.NUM_STANDARD_DEVIATIONS)

# set values below threshold to 0
output_string += "Threshold: " + str(threshold) + "\n"
for i in xrange(distances.__len__()):
    for j in xrange(distances[0].__len__()):
        if distances[i][j] > threshold:
            distances[i][j] = 1
        elif settings.THRESHOLD_MAKE_BINARY:
            distances[i][j] = 1
        distances[i][j] = 1 - distances[i][j]

count_nonzero = 0
count_most_dissimilar = 0
for i in xrange(distances.__len__()):
    for id in distances[i]:
        if id > 0:
            count_nonzero += 1
        if abs(id - most_dissimilar) < 0.001:
            count_most_dissimilar += 1
output_string += "Non-zero distances: " + str(count_nonzero) + "\n"\
                 "Most dissimilar (min) distance: " + str(most_dissimilar) + "\n"\
                 "Number of most dissimilar: " + str(count_most_dissimilar) + "\n"

settings.output(distances, "clipped_distances+SD"+str(settings.NUM_STANDARD_DEVIATIONS), ext=".dat", mode="savetxt")

total_seconds = time.time() - start_time
output_string += "Finished 'set_threshold.py' in " + str(total_seconds) + " seconds!"
settings.output(output_string, "stats_post_threshold"+str(settings.NUM_STANDARD_DEVIATIONS), mode="write")
print "Finished 'set_threshold.py' in " + str(total_seconds) + " seconds!"