__author__ = 'VestalNetSciHigh'

""" Setup global constants and define functions """

import os
from numpy import savetxt
import itertools
import collections

# path to data directory, target file (csv file, without extension), output directory
PATH = "..\\data"
TARGET = "NetSci-Data-15w04f"
OUTPUT = "..\\output\\" + TARGET[12:]

NUM_STANDARD_DEVIATIONS = 2  # Set the SD offset for the threshold

THRESHOLD_MAKE_BINARY = False  # set distances above THRESHOLD to 1

ID_STRING_KEY = "unitid"
ATTRIBUTE_STRING_KEYS = [
    ['institution name', 'Name'],
    ['EF2013D.Student-to-faculty ratio', 'Student-to-faculty ratio'],
    ['DRVIC2013.Tuition and fees, 2013-14', 'Cost'],
    ['HD2013.Institution size category', 'Institution Size'],
    ['HD2013.FIPS state code', 'State'],
    ['HD2013.Geographic region', 'Geographic Region'],
    ['HD2013.Level of institution', 'Level of Institution'],
    ['HD2013.Control of institution', 'Control of Institution'],
    ['HD2013.Degree-granting status', 'Degree-granting Status'],
    ['HD2013.Historically Black College or University', 'Historically Black College or University'],
    ['HD2013.Tribal college', 'Tribal college'],
    ['HD2013.Degree of urbanization (Urban-centric locale)', 'Degree of urbanization (Urban-centric locale)'],
    ['HD2013.Institutional category', 'Institutional category'],
    ['HD2013.Carnegie Classification 2010: Basic', 'Carnegie Classification 2010: Basic'],
    ['HD2013.Carnegie Classification 2010: Undergraduate Instructional Program', 'Carnegie Classification 2010: Undergraduate Instructional Program'],
    ['HD2013.Carnegie Classification 2010: Graduate Instructional Program', 'Carnegie Classification 2010: Graduate Instructional Program'],
    ['HD2013.Carnegie Classification 2010: Undergraduate Profile', 'Carnegie Classification 2010: Undergraduate Profile'],
    ['HD2013.Carnegie Classification 2010: Enrollment Profile', 'Carnegie Classification 2010: Enrollment Profile'],
    ['HD2013.Carnegie Classification 2010: Size and Setting', 'Carnegie Classification 2010: Size and Setting'],
    ['HD2013.Land Grant Institution', 'Land Grant Institution'],
    ['HD2013.Carnegie Classification 2000', 'Carnegie Classification 2000'],
    ['HD2013.Data Feedback Report comparison group category created by NCES', 'Data Feedback Report comparison group category created by NCES'],
]


if not os.path.exists(OUTPUT):
        os.makedirs(os.path.abspath(OUTPUT))


def output(content, filename=TARGET, ext=".txt", mode="print", charlimit=0, print_in_console=False, overwrite=True):
    """
    Write to a file.

    Parameters:          content: string or other output stream
                        filename: name of the output file
                             ext: file extension
                            mode: "print" | "write" | "savetxt", denotes which method to use when writing to file.
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
    elif mode == "print":
        print >> f, content
    elif mode == "savetxt":
        savetxt(OUTPUT + "\\" + filename + ext, content)

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
    bins += 1

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


# custom distance metric, searches per category: number of matches / total possible matches
def distance(array_one, array_two):
    num_categories = sum(array_one)
    if not array_one.__len__() == array_two.__len__():
        raise Exception("Arrays must be the same length.")
    ntt = 0  # count the number of dimensions in which both values are True
    for i in xrange(array_one.__len__()):
        if (array_one[i] == 1) and (array_two[i] == 1):
            ntt += 1
    return 1 - (float(ntt) / num_categories)


def skip(iterable, at_start=0, at_end=0):
    it = iter(iterable)
    for x in itertools.islice(it, at_start):
        pass
    queue = collections.deque(itertools.islice(it, at_end))
    for x in it:
        queue.append(x)
        yield queue.popleft()