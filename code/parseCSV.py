__author__ = 'VestalNetSciHigh'

# Todo 0: create our own metric for [0, 1] (with own normalization -> using scipy)
# NTT / number of categories     where NTT = number of dims in which both values are True
# number of Trues (if True sum += 1)    <- test function check for same num trues in each row
# http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html
# https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/neighbors/dist_metrics.pyx
# http://docs.scipy.org/doc/numpy/reference/generated/numpy.array.html

# Todo 1: scikit-lean distance metric used to generate a n*n matrix (each element of the sparce_matrix against every other) (numpy format)
# Todo 2: Determine the threshold for the matrix
# Todo 3: Set matrix values to 0 that fall below the threshold
# Todo 4: Generate a network using networkx using the matrix as the adjacency matrix (networkx takes numpy matrix format)
# Note: labels for the nodes in the network will be lost in the above process.  You will need to keep track of the
# university name and it's specific position in the matrix
# Note #2: (maybe, if networkx doesn't take real valued adjacency): above threshold to 1
# Todo 5: Save network in a "Gephiable" data format

import csv
import os
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import DistanceMetric
import networkx as nx


# path to data directory, target file (csv file, without extension), output directory
PATH = "..\\data"
TARGET = "Test-Data-15w09c"
OUTPUT = "..\\output"


def output(content, filename=TARGET, ext=".txt", mode="print", charlimit=0, print_in_console=False, overwrite=True):
    """
    Write to a file.

    Parameters:          content: string or other output stream
                        filename: name of the output file
                             ext: file extension
                            mode: "print" | "write", denotes which method to use when writing to file.
                       charlimit: limits the number of characters to write, 0 for unlimited.
                print_in_console: when True, also print output in the console.
                       overwrite: when True, allows existing files to be overwritten.
    """

    if not os.path.exists(OUTPUT):
        os.makedirs(os.path.abspath(OUTPUT))
    else:
        if os.path.exists(OUTPUT+"\\"+filename+ext):
            if overwrite:
                print filename+ext + " already exists! Overwriting."
            else:
                print filename+ext + " already exists! Terminating write operation."
                return  # Terminate function: Avoid overwrite.
    if charlimit > 0:
        content = content[:charlimit]

    f = open(OUTPUT + "\\" + filename + ext, 'w')
    if mode == "write":
        f.write(content)
    else:
        print >> f, content

    if print_in_console:
        print filename + ext
        print content


def numerical_to_categorical(value, interval, bins, unit='', prefix_unit=False):
    """
    Returns a String representing which bin numerical data falls into, meant to replace the numerical data.

    Parameters:       value: numerical data to be replaced
                   interval: bin width
                       bins: number of bins for sorting

                  (optional)
                       unit: a symbol or small String to be used as a prefix or postfix, see Boolean prefix_unit
                prefix_unit: When True, prepend unit symbol, or else append it.
    """

    final_string = ""

    def get_category_bins(width, position, _unit='', _prefix_unit=False):
        """
        Returns a String representing which bin numerical data falls into, meant to replace the numerical data.

        Parameters:       width: bin width, good values are approximately 2 * n * IQR^(-1/3)
                       position: Designates which bin for which to build a String. A 0 denotes that the category
                                 should read "Less than" the lowest bin, and -1 is reserved for "Greater than"
                                 the highest bin specified.

                      (optional)
                          _unit: a symbol or small String to be used as a prefix or postfix, see Boolean prefix_unit
                   _prefix_unit: When True, prepend unit symbol, or else append it.
        """

        if position < 1:
            _bin = "{:,}".format(width)
            return ("Less than " if position == 0 else "Greater than ") + \
                   (_unit+_bin if _prefix_unit else _bin+" "+_unit)
        else:
            _min_num = "{:,}".format(width * position)
            _max_num = "{:,}".format(width * (position + 1) - 1)
            if _prefix_unit:
                return _unit+_min_num + " - " + _unit+_max_num
            else:
                return _min_num+" "+_unit + " - " + _max_num+" "+_unit

    is_converted = False  # True when numerical to categorical conversion is successful
    for pos in range(0, bins - 1):
        if int(value) < interval * (pos + 1):
            final_string = get_category_bins(interval, pos, _unit=unit, _prefix_unit=prefix_unit)
            is_converted = True
            break
    if not is_converted:  # Final category
        final_string = get_category_bins(interval * (bins - 1), -1, _unit=unit, _prefix_unit=prefix_unit)

    return final_string

# begin program
csvfile = open(PATH + "\\" + TARGET + ".csv")
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
    row[tuition_key] = numerical_to_categorical(row[tuition_key], 5000, 3, unit='$', prefix_unit=True)

    # duplicate row handling
    if key in data:
        print "WARNING: duplicate key: " + key
        pass

    data[key] = row

# dict to "one-hot" format
vec = DictVectorizer()
sparse_matrix = vec.fit_transform(data.itervalues()).toarray()
print sparse_matrix

# insure same number of categories in each row
num_trues = []
for row in sparse_matrix:
    num_trues.append((sum(row)))
num_categories = num_trues[0]
for val in num_trues:
    if not (num_categories == val):
        raise Exception("Mismatch in number of categories!")

# out custom distance metric
def distance(array_one, array_two):
    if not array_one.__len__() == array_two.__len__():
        raise Exception("Arrays must be the same length.")
    ntt = 0  # count the number of dimensions in which both values are True
    for i in range(0, array_one.__len__() - 1):
        if (array_one[i] == 1) and (array_two[i] == 1):
            ntt += 1
    return ntt / num_categories

# generate distances
distance_calculator = DistanceMetric.get_metric(distance)
distances = distance_calculator.pairwise(sparse_matrix)

# compute average distances
distance_list = distances.tolist()
average_similarity = []
for index in range(0, sparse_matrix.__len__() - 1):
    average_similarity.append(sum(distance_list[index]) / distance_list[index].__len__())
sum_of_averages = 0
for value in average_similarity:
    sum_of_averages += sum(distance_list[index])

average_distance = sum_of_averages / average_similarity.__len__()
print "Average distance: " + str(average_distance)

# set values below threshold to 0
threshold = 0.40
for count in range(0, distances[0].__len__()):
    print str(distances[0][count])
    if distances[0][count] <= threshold:
        print "Below Threshold"
        distances[0][count] = 0
print distances[0]

# Create a networkx graph
G = nx.from_numpy_matrix(distances)
# print G.edges()

print "Number of categories: " + str(num_categories)