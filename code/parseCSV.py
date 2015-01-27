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
                return
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


# def get_bins(position, width):
#     yield position * width

def print_this_thing_quickly(text):
    print text


# begin program
csvfile = open(PATH + "\\" + TARGET + ".csv")
reader = csv.DictReader(csvfile)

# CSV to dict
data = {}
tuition_key = 'DRVIC2013.Tuition and fees, 2013-14'  # numerical to categorical
for row in reader:
    row.pop('unitid')  # unnecessary unique ID
    key = row.pop('institution name')

    # Break Tuition cost into categories. Intervals of 5k.
    row[tuition_key] = "Less than $5,000" if row[tuition_key] < 5000 else row[tuition_key]
    row[tuition_key] = "$5,000 - $9,999" if row[tuition_key] < 10000 else row[tuition_key]
    row[tuition_key] = "$10,000 - $14,999" if row[tuition_key] < 15000 else row[tuition_key]
    row[tuition_key] = "$15,000 - $19,999" if row[tuition_key] < 20000 else row[tuition_key]
    row[tuition_key] = "$20,000 - $24,999" if row[tuition_key] < 25000 else row[tuition_key]
    row[tuition_key] = "$25,000 - $29,999" if row[tuition_key] < 30000 else row[tuition_key]
    row[tuition_key] = "$30,000 - $34,999" if row[tuition_key] < 35000 else row[tuition_key]
    row[tuition_key] = "$35,000 - $39,999" if row[tuition_key] < 40000 else row[tuition_key]
    row[tuition_key] = "$40,000 - $44,999" if row[tuition_key] < 45000 else row[tuition_key]
    row[tuition_key] = "$45000 - $49999" if row[tuition_key] < 50000 else row[tuition_key]

    print row[tuition_key]

    # duplicate row handling
    if key in data:
        print "WARNING: 'unitid' duplicate: " + key
        pass
    data[key] = row

output(json.dumps(data), filename=TARGET[12:]+"_dict", ext=".json", print_in_console=True)

# dict to "one-hot" format
vec = DictVectorizer()
sparse_matrix = vec.fit_transform(data.itervalues()).toarray()
feature_names = vec.get_feature_names()


# output(sparse_matrix, filename=TARGET[12:]+"_matrix", ext=".txt", print_in_console=True)
# output(feature_names, filename=TARGET[12:]+"_features", ext=".txt", print_in_console=True)
