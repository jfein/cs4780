import math
import cPickle as pickle

cache_file = "cache.dat"
CACHE = {}


def load_cache(sim_func_str):
    global CACHE
    try:
        f = open(sim_func_str + " _ " + cache_file, 'rb')
        CACHE = pickle.load(f)
        f.close()
    except IOError as e:
        CACHE = {}


def save_cache(sim_func_str):
    f = open(sim_func_str + " _ " + cache_file, 'wb')
    pickle.dump(CACHE, f, protocol=2)
    f.close()


def cache_gen_key(u1, u2, type):
    s = sorted([u1, u2])
    return "{0}-{1}-{2}".format(s[0], s[1], type)


def cache_get(u1, u2, type):
    return CACHE.get(cache_gen_key(u1, u2, type))


def cache_set(u1, u2, type, v):
    global CACHE
    k = cache_gen_key(u1, u2, type)
    CACHE[k] = v


def inverse_euclidean(u1, v1, u2, v2):
    cache = cache_get(u1, u2, 'inverse_euclidean')
    if cache is not None:
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

    cache_set(u1, u2, 'inverse_euclidean', ret)
    return ret


def dot_product(u1, v1, u2, v2):
    cache = cache_get(u1, u2, 'dot_product')
    if not cache is None:
        return cache

    dp = 0.0
    # Pass through v1
    for song_id, plays in v1.iteritems():
        dp += plays * v2.get(song_id, 0)
    # Pass through v2
    for song_id, plays in v2.iteritems():
        if not song_id in v1:
            dp += v1.get(song_id, 0) * plays

    cache_set(u1, u2, 'dot_product', dp)
    return dp


def cos(u1, v1, u2, v2):
    cache = cache_get(u1, u2, 'cos')
    if cache is not None:
        return cache

    magnitude_v1 = 0.0
    magnitude_v2 = 0.0
    for plays in v1.values():
        magnitude_v1 += plays ** 2

    for plays in v2.values():
        magnitude_v2 += plays ** 2

    magnitude_v1 = math.sqrt(magnitude_v1)
    magnitude_v2 = math.sqrt(magnitude_v2)

    ret = dot_product(u1, v1, u2, v2) / (magnitude_v1 * magnitude_v2)

    cache_set(u1, u2, 'cos', ret)
    return ret
