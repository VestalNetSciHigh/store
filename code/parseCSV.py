__author__ = 'VestalNetSciHigh'

""" Read in data via a .csv file, verify data integrity, calculate distance metrics for each element, and output """

import csv
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import DistanceMetric
import time
import settings

start_time = time.time()
csvfile = open(settings.PATH + "\\" + settings.TARGET + ".csv")
reader = csv.DictReader(csvfile)

# CSV to dict
data = {}

tuition_key = 'DRVIC2013.Tuition and fees, 2013-14'  # to be converted: numerical to categorical
for row in reader:
    key = row.pop('unitid')
    if key == '':
        continue
    # key = row.pop('institution name')  # There exist multiple institutions with the same name but different locations.

    # Assign a categorical tuition cost
    row[tuition_key] = settings.numerical_to_categorical(row[tuition_key], 5000, 11, unit='$', prefix_unit=True)

    # duplicate row handling
    if key in data:
        print "WARNING: duplicate key: " + key
        pass

    data[key] = row
print "Number of elements: " + str(data.__len__())

# dict to "one-hot" format
vec = DictVectorizer()
sparse_matrix = vec.fit_transform(data.itervalues()).toarray()

# insure same number of categories in each row
num_trues = []
for row in sparse_matrix:
    num_trues.append((sum(row)))
num_categories = num_trues[0]
for val in num_trues:
    if not (num_categories == val):
        raise Exception("Mismatch in number of categories!")

print "Number of categories (denominator): " + str(int(num_categories))

# generate distances
distance_calculator = DistanceMetric.get_metric(settings.distance)
distances = distance_calculator.pairwise(sparse_matrix)

settings.output(distances, "real_distances", ext=".dat", mode="savetxt")

total_seconds = time.time() - start_time
print "Finished 'parseCSV.py' in " + str(total_seconds) + " seconds!"

