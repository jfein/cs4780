import math


CACHE = {}


def cache_gen_key(u1, u2):
    s = sorted([u1, u2])
    return "{0}-{1}".format(s[0], s[1])
    
    
def cache_get(u1, u2):
    return CACHE.get(cache_gen_key(u1, u2))

    
def cache_set(u1, u2, v):
    global CACHE
    k = cache_gen_key(u1, u2)
    CACHE[k] = v

    
def inverse_euclidean(u1, v1, u2, v2, use_cache=True):
    cache = cache_get(u1, u2)
    if cache is not None and use_cache:
        return cache

    squared_sum = 0.0
    # Pass through v1
    for song_id, plays in v1.iteritems():
        unquared_sum = (plays - v2.get(song_id, 0))
        squared_sum += unquared_sum ** 2
    # Pass through v2
    for song_id, plays in v2.iteritems():
        if not song_id in v1:
            squared_sum += plays ** 2

    if squared_sum == 0:
        ret = 1
    else:
        ret = 1 / math.sqrt(squared_sum)
        
    cache_set(u1, u2, ret)
    return ret

    
def dot_product(u1, v1, u2, v2, use_cache=True):
    cache = cache_get(u1, u2)
    if not cache is None and use_cache:
        return cache
        
    dp = 0.0
    # Pass through v1
    for song_id, plays in v1.iteritems():
        dp += plays * v2.get(song_id, 0)
    # Pass through v2
    for song_id, plays in v2.iteritems():
        if not song_id in v1:
            dp += v1.get(song_id, 0) * plays
            
    cache_set(u1, u2, dp)
    return dp

    
def cos(u1, v1, u2, v2, use_cache=True):
    cache = cache_get(u1, u2)
    if cache is not None and use_cache:
        return cache
        
    magnitude_v1 = 0.0
    magnitude_v2 = 0.0
    for plays in v1.values():
        magnitude_v1 += plays ** 2

    for plays in v2.values():
        magnitude_v2 += plays ** 2

    magnitude_v1 = math.sqrt(magnitude_v1)
    magnitude_v2 = math.sqrt(magnitude_v2)

    ret = dot_product(u1, v1, u2, v2, False) / (magnitude_v1 * magnitude_v2)
    
    cache_set(u1, u2, ret)
    return ret
