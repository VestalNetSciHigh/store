__author__ = 'Ryan'

# http://stackoverflow.com/questions/14683690/machine-learning-email-prioritization-python

import csv
import os
import scipy

# path to data folder
path = "C:\\Users\\Ryan\\Documents\\Netsci High\\Project\\data"
filename = "NetSci-Data-15w04e_TEMP.csv"

# if os.path.exists(path+"\\"+filename):
csvfile = open(path+"\\"+filename)
datafile = csv.reader(csvfile)

dicts = []
y = []

for row in datafile:
    y.append(row[-1])
    d = {"From": row[0]}
    for word in row[1]:
        d["Subject_" + word] = 1
    for word in row[2]:
        d["Body_" + word] = 1
    # etc.
    dicts.append(d)

print dicts

# vectorize!
#vectorizer = DictVectorizer()
#X_train = vectorizer.fit_transform(dicts)

#def split_words(string):
    # not implemented



