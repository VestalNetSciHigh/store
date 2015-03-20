__author__ = 'VestalNetSciHigh'

""" Read in data via a .csv file, verify data integrity, calculate distance metrics for each element, and output """

from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import DistanceMetric
import settings
import time
import csv

start_time = time.time()
csvfile = open(settings.PATH + "\\" + settings.TARGET + ".csv")
reader = csv.DictReader(csvfile)

# CSV to dict
data = {}
names = []
for row in reader:
    key = row.pop(settings.ID_STRING_KEY)
    if key == '':
        continue
    # key = row.pop(name_string_key)  # There exist multiple institutions with the same name but different locations.

    # Assign a categorical tuition cost
    row[settings.TUITION_KEY] = \
        settings.numerical_to_categorical(row[settings.TUITION_KEY], 5000, 11, unit='$', prefix_unit=True)

    # duplicate row handling
    if key in data:
        print "WARNING: duplicate key: " + key
        pass

    data[key] = row
    names.append(row.pop(settings.NAME_STRING_KEY))

print "Number of elements: " + str(data.__len__())

# save reordered dict as a new .csv (only two columns)
w = csv.writer(open(settings.OUTPUT+"\\dict_data.dat", "w"))
w.writerow([settings.ID_STRING_KEY, data.keys()])
data
for key, vals in data.items():
    line = []
    line.append(key)
    line.extend(vals.values())
    w.writerow(line)

# extract unitid from reordered dict (order was not preserved)
r = csv.DictReader(open(settings.OUTPUT+"\\dict_data.dat"))
w = csv.writer(open(settings.OUTPUT+"\\dict_data_selective_attributes.dat", "w"))
w.writerow([settings.ID_STRING_KEY, settings.NAME_STRING_KEY])
count = 0
for row in r:
    w.writerow([row.pop(settings.ID_STRING_KEY), names[count]])
    count += 1

# dict to "one-hot" format (order assumed to be preserved)
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

