__author__ = 'VestalNetSciHigh'

# Helpful links: StackOverFlow is life!
# http://stackoverflow.com/questions/14683690/machine-learning-email-prioritization-python
# http://stackoverflow.com/questions/14091387/creating-a-dictionary-from-a-csv-file
# http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary

import csv
import os
import json
from sklearn.feature_extraction import DictVectorizer


# path to data directory, target file (csv file, without extension), output directory
PATH = "..\\data"
TARGET = "NetSci-Data-15w04f"
OUTPUT = "..\\output"


def output(content, filename=TARGET, ext=".txt", charlimit=0, print_in_console=False, overwrite=True):
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
    # write(content)
    print >> f, content

    if print_in_console:
        print filename + ext
        print content


# begin program
csvfile = open(PATH + "\\" + TARGET + ".csv")
reader = csv.DictReader(csvfile)

# CSV to dict
data = {}
for row in reader:
    key = row.pop('unitid')
    # duplicate row handling
    if key in data:
        print "WARNING: 'unitid' duplicate: " + key
        pass
    data[key] = row
output(json.dumps(data), filename=TARGET[12:]+"_dict", ext=".json")

# dict to "one-hot" format
vec = DictVectorizer()
sparse_matrix = vec.fit_transform(data.itervalues()).toarray()

output(sparse_matrix, filename=TARGET[12:]+"_matrix", ext=".txt", charlimit=0, print_in_console=True)
