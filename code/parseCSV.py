__author__ = 'VestalNetSciHigh'

#Todo_1: scikit-lean distance metric used to generate a n*n matrix (each element of the sparce_matrix against every other) (numpy format)

#Todo_2: Determine the threshold for the matrix

#Todo_3: Set matrix values to 0 that fall below the threshold

#Todo_4: Generate a network using networkx using the matrix as the adjacency matrix (networkx takes numpy matrix format)
#Note: labels for the nodes in the network will be lost in the above process.  You will need to keep track of the university name
#and it's specific position in the matrix

#Todo_5: Save network in a "Gephiable" data format

import csv
import os
import json
from sklearn.feature_extraction import DictVectorizer


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


def get_category_bins(width, position, unit='', prefix_unit=False):
    """
    Description

    Parameters:       width:
                   position:
                       unit:
                prefix_unit:
    """

    if position < 1:
        bin = "{:,}".format(width)
        return ("Less than " if position == 0 else "Greater than ") + \
               (unit+bin if prefix_unit else bin+" "+unit)
    else:
        min_num = (unit+str(width * position) if prefix_unit else str(width * position)+" "+unit)
        max_num = (unit+str(width * (position + 1) - 1) if prefix_unit else str(width * (position + 1) - 1)+" "+unit)
        return min_num + " - " + max_num
        # todo: add 1000 comma separators to result strings


# begin program
csvfile = open(PATH + "\\" + TARGET + ".csv")
reader = csv.DictReader(csvfile)

# CSV to dict
data = {}

tuition_key = 'DRVIC2013.Tuition and fees, 2013-14'  # numerical to categorical
tuition_interval = 5000  # bins for categorical conversion
tuition_bins = 10  # number of bins (each with a width of "tuition_interval"
for row in reader:
    key = row.pop('unitid')
    # key = row.pop('institution name')  # There exist multiple institutions with the same name but different locations.

    # Assign a categorical tuition cost
    isConverted = False  # True when numerical to categorical conversion is successful
    for pos in range(0, tuition_bins - 1):
        if int(row[tuition_key]) < tuition_interval * (pos + 1):
            row[tuition_key] = get_category_bins(tuition_interval, pos, unit='$', prefix_unit=True)
            isConverted = True
            break
    if not isConverted:  # Final category
        row[tuition_key] = get_category_bins(tuition_interval * (tuition_bins - 1), -1, unit='$', prefix_unit=True)

    # duplicate row handling
    if key in data:
        print "WARNING: duplicate key: " + key
        pass

    data[key] = row
    print row[tuition_key]

# output(json.dumps(data), filename=TARGET[12:]+"_dict", ext=".json")

# dict to "one-hot" format
vec = DictVectorizer()
sparse_matrix = vec.fit_transform(data.itervalues()).toarray()
# output(sparse_matrix, filename=TARGET[12:]+"_matrix", ext=".txt", print_in_console=True)

feature_names = vec.get_feature_names()  # not required
# output(feature_names, filename=TARGET[12:]+"_features", ext=".txt", print_in_console=True)

