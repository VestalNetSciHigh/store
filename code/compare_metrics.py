__author__ = 'Chris'

# New approach:
# Our criteria: N, NTF, NFT, NNEQ
# Our rationale: We should not distinguish between NTT and NFF for our data.
#
# Matching Distance: NNEQ / N
#  - similar as distance -> 1-
#  - linear (same denominator), can compare distances to distances
#
# Rogers Tanimoto Distance: 2 * NNEQ / (N + NNEQ)
#  Sokal Michener Distance: 2 * NNEQ / (N + NNEQ)
#  - similar as distance  -> 0+
#  - non-linear


def rogers_tanimoto_distance(function, num_similar, num_total):
    if function == "rogersTanimoto":
        return 2 * (num_total - num_similar) / float(num_total + (num_total - num_similar))
    if function == "matching":
        return (num_total - num_similar) / float(num_total)


total = 50
for x in range(0, total + 1):
    # print str(x) + "/" + str(total) + ": " + str(metric(x, total))
    print str(rogers_tanimoto_distance("matching", x, total))
