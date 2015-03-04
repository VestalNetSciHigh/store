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

# Configurable Constants
THRESHOLD = 0.33  # set all distance below this number to 0
MAKE_BINARY = False  # set distances above THRESHOLD to 1

start_time = time.time()
output_string = ""

# load output from parseCSV.py
distances = loadtxt(settings.OUTPUT+"\\real_distances.dat")

# load output from calculate_stats.py (if exists)
most_dissimilar = 0
if os.path.exists(settings.OUTPUT+"\\"+"most_dissimilar.dat"):
    most_dissimilar = loadtxt(settings.OUTPUT+"\\most_dissimilar.dat")

# set values below threshold to 0
output_string += "Threshold: " + str(THRESHOLD) + "\n"
for i in xrange(distances.__len__()):
    for j in xrange(distances[0].__len__()):
        if distances[i][j] < THRESHOLD:
            distances[i][j] = 0
        elif MAKE_BINARY:
            distances[i][j] = 1

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

settings.output(distances, "clipped_distances", ext=".dat", mode="savetxt")

total_seconds = time.time() - start_time
output_string += "Finished 'set_threshold.py' in " + str(total_seconds) + " seconds!"
settings.output(output_string, "stats_post_threshold", mode="write")
print "Finished 'set_threshold.py' in " + str(total_seconds) + " seconds!"