import heapq
import random
import operator
import time

from util import *


DISTANCE_CACHE = {}
SONG_DATA = load_song_data('song_mapping.txt')
training = parse_training('user_train.txt')
test = parse_test('user_test.txt')

def find_knn(k, test_vector, training_examples, sim_func):
    '''
    Find the k nearest neighbors of test_vector in the
    training_examples. Distance is determined
    by sim_func. Sim_func must be a function that
    takes in two vectors Represented by dictionaries of
    song id -> number of times played)
    and returns a distance, with lower being closer

    returns a list of (dist, example) pairs for 
    the k nearest neighbors
    '''

    # Go through and compute distances b/w
    # test vector and every training example,
    # placing results on a heap so we can
    # easily extract k nearest afterwards
    heap = []
    for example in training_examples:
        dist = sim_func(test_vector, example)
        #heapq.heappush(heap, (dist, example))
        heap.append((dist, example))

    return heapq.nsmallest(k, heap, key=operator.itemgetter(0))


def construct_ranking_vector(knn_pairs, use_weighted):
    '''
    Construct the ranking vector R.
    @param knn_pairs: A list of (dist, example) pairs where
    example is one of the knn training examples and dist
    is the distance between the example and the test vector
    @param weighted: True if we should use weighted knn
    to construct R

    Returns the ranking vector R, which is a dictionary
    mapping song_id to rank
    '''

    R = {}
    k = float(len(knn_pairs))
    total_dist = 0.0
    for dist, example in knn_pairs:
        total_dist += dist
        for song_id, plays in example.iteritems():
            old_ranking = R.get(song_id, 0)
            if use_weighted:
                updated_ranking = old_ranking + dist * plays
            else:
                updated_ranking = old_ranking + plays
            R[song_id] = updated_ranking

    # Now we need to go through and normalize everything
    # If we're not using weighted then we divide everything
    # by k. If we are we divide by the total distance
    for song_id, rank in R.iteritems():
        if use_weighted:
            R[song_id] = rank / total_dist
        else:
            R[song_id] = rank / k

    return R


def recommend_songs(k, test_vector, training_examples, sim_func, use_weighted):
    '''
    Returns a list of the top 10 recommended songs
    '''
    start = time.time()
    knn_pairs = find_knn(k, test_vector, training_examples, sim_func)
    after_knn = time.time()
    print 'finding knn took', after_knn - start, 'seconds'
    R = construct_ranking_vector(knn_pairs, use_weighted)
    after_r = time.time()
    print 'constructing r took', after_r - after_knn, 'seconds'

    # Now we just sort recommendations
    # and take the top 10, making sure to 
    # check that the user hasn't already played that song

    sorted_R = sorted(R.iteritems(), key=operator.itemgetter(1))
    recommendations = []
    while len(recommendations) < 10 and len(sorted_R) > 0:
        recommendation, _ = sorted_R.pop()
        if recommendation not in test_vector:
            recommendations.append(recommendation)

    print 'finding top 10 recommendations took', time.time() - after_r, 'seconds'
    return recommendations


def user_query(user_id, k, sim_func, use_weighted):
    test_vector = training[user_id]
    del training[user_id]
    training_examples = training.values()

    # Go through and find the most played songs for user
    most_played = sorted(test_vector.iteritems(), key=operator.itemgetter(1),
                          reverse=True)
    print 'Most played for user', user_id
    print "Song ID\tTitle\tArtists\tPlays"
    for song_id, plays in most_played[:10]:
        title, artist = SONG_DATA[song_id]
        print song_id, "\t", title, "\t", artist, '\t', plays

    recommendations = recommend_songs(k, test_vector, training_examples, sim_func, use_weighted)
    print "\n\nTop 10 Recommended Songs for user ", user_id
    print "Song ID\tTitle\tArtists\t"
    for song_id in recommendations:
        title, artist = SONG_DATA[song_id]
        print song_id, "\t", title, "\t", artist


def baseline_random():
    # first we need to get all the song ids
    song_ids = set()
    training_examples = training.values()
    for training_example in training_examples:
        for song_id in training_example.keys():
            song_ids.add(song_id)

    for test_example in test.values():
        for song_id in test_example:
            song_ids.add(song_id)

    total_prec_at_10 = 0.0
    for _, ommitted_songs in test.items():
        recomendations = random.sample(song_ids, 10)
        matched = 0
        for recommendation in recomendations:
            if recommendation in ommitted_songs:
                matched += 1

        total_prec_at_10 += matched / 10.0

    print 'Average Precision at 10 using random = ', \
           total_prec_at_10 / len(test)


def baseline_most_popular():
    song_totals = {}
    for song_map in training.values():
        for song_id, plays in song_map.iteritems():
            song_totals[song_id] = song_totals.get(song_id, 0) + plays

    sorted_totals = sorted(song_totals.iteritems(), key=operator.itemgetter(1),
                           reverse=True)
    recommendations = [song for song, _ in sorted_totals[:10]]

    total_prec_at_10 = 0.0
    for _, ommitted_songs in test.items():
        matched = 0
        for recommendation in recommendations:
            if recommendation in ommitted_songs:
                matched += 1

        total_prec_at_10 += matched / 10.0

    print 'Average Precision at 10 using most popular = ', \
           total_prec_at_10 / len(test)


def baseline_knn(k, sim_func, use_weighted):
    total_prec_at_10 = 0.0
    counter = 0
    print len(training)
    for user_id, test_vector in training.iteritems():
        counter += 1
        if counter % 100 == 0:
            print counter
        recommendations = recommend_songs(k, test_vector, training.values(),
                                          sim_func, use_weighted)

        matched = 0
        for recommendation in recommendations:
            if recommendation in test[user_id]:
                matched += 1
        total_prec_at_10 += matched / 10.0

    prec_at_10 = total_prec_at_10 / len(training)

    return prec_at_10
