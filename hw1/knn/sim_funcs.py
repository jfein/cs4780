'''
Created on Sep 4, 2012

@author: Will
'''

import math

def inverse_euclidean(v1, v2):
    squared_sum = 0.0
    # Pass through v1
    for song_id, plays in v1.iteritems():
        unquared_sum = (plays - v2.get(song_id, 0))
        squared_sum += unquared_sum ** 2
    # Pass through v2
    for sing_id, plays in v2.iteritems():
        if not song_id in v1:
            unquared_sum = (v1.get(song_id, 0) - plays)
            squared_sum += unquared_sum ** 2

    if squared_sum == 0:
        return 1
    else:
        return 1 / math.sqrt(squared_sum)

def dot_product(v1, v2):
    keys = set(v1.keys() + v2.keys())
    dp = 0.0
    for song_id in keys:
        dp += v1.get(song_id, 0) * v2.get(song_id, 0)

    return dp

def cos(v1, v2):
    magnitude_v1 = 0.0
    magnitude_v2 = 0.0
    for plays in v1.values():
        magnitude_v1 += plays ** 2

    for plays in v2.values():
        magnitude_v2 += plays ** 2

    magnitude_v1 = math.sqrt(magnitude_v1)
    magnitude_v2 = math.sqrt(magnitude_v2)

    return dot_product(v1, v2) / (magnitude_v1 * magnitude_v2)
