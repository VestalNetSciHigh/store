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
# Todo 5: Save network in a "Gephiable" data format

import csv
import os
import json
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import DistanceMetric


# path to data directory, target file (csv file, without extension), output directory
PATH = "..\\data"
TARGET = "NetSci-Data-15w04f"
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
    # key = row.pop('institution name')  # There exist multiple institutions with the same name but different locations.

    # Assign a categorical tuition cost
    row[tuition_key] = numerical_to_categorical(row[tuition_key], 5000, 10, unit='$', prefix_unit=True)

    # duplicate row handling
    if key in data:
        print "WARNING: duplicate key: " + key
        pass

    data[key] = row

# output(json.dumps(data), filename=TARGET[12:]+"_dict", ext=".json")  # output intermediary step

# dict to "one-hot" format
vec = DictVectorizer()
sparse_matrix = vec.fit_transform(data.itervalues()).toarray()
output(sparse_matrix, filename=TARGET[12:]+"_matrix", mode="write", ext=".txt", print_in_console=True)  # output intermediary step

feature_names = vec.get_feature_names()  # not required, just for inspection
# output(feature_names, filename=TARGET[12:]+"_features", ext=".txt", print_in_console=True)  # output intermediary step

dist = DistanceMetric.get_metric('kulsinski')
distances = dist.pairwise(sparse_matrix)
output(distances, filename=TARGET[12:]+"_distances", mode="write", ext=".txt", print_in_console=True)
