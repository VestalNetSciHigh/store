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
attributes = []
for row in reader:
    key = row.pop(settings.ID_STRING_KEY)
    if key == '':
        continue
    # key = row.pop(name_string_key)  # There exist multiple institutions with the same name but different locations.

    # Assign a categorical tuition cost
    row[settings.ATTRIBUTE_STRING_KEYS[2]] = \
        settings.numerical_to_categorical(row[settings.ATTRIBUTE_STRING_KEYS[2]], 5000, 11, unit='$', prefix_unit=True)

    # duplicate row handling
    if key in data:
        print "WARNING: duplicate key: " + key
        pass

    data[key] = row
    '''
    row_attributes = [key]
    for i in xrange(settings.ATTRIBUTE_STRING_KEYS.__len__()):
        row_attributes.append(row.pop(settings.ATTRIBUTE_STRING_KEYS[i]))
    attributes.append(row_attributes)
    '''

print data

print "Number of elements: " + str(data.__len__())

'''
# save reordered dict as a new .csv (only two columns)
w = csv.writer(open(settings.OUTPUT+"\\dict_data.dat", "w"))
w.writerow([settings.ID_STRING_KEY, 'val'])
for key, val in data.items():
    w.writerow([key, val])
'''

# extract unitid from reordered dict (order was not preserved)
# r = csv.DictReader(open(settings.OUTPUT+"\\dict_data.dat"))
w = csv.writer(open(settings.OUTPUT+"\\dict_data_selective_attributes.dat", "w"))
row_header = [settings.ID_STRING_KEY]
for i in xrange(settings.ATTRIBUTE_STRING_KEYS.__len__()):
    row_header.append(settings.ATTRIBUTE_STRING_KEYS[i])
w.writerow(row_header)
for row in attributes:
    w.writerow(row)

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

print sparse_matrix

# generate distances
distance_calculator = DistanceMetric.get_metric(settings.distance)
distances = distance_calculator.pairwise(sparse_matrix)

settings.output(distances, "real_distances", ext=".dat", mode="savetxt")

total_seconds = time.time() - start_time
print "Finished 'parseCSV.py' in " + str(total_seconds) + " seconds!"

