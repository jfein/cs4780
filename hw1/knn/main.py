'''
Created on Sep 4, 2012

@author: Will
'''
from knn import *

def print_usage_and_quit():
    print 'Usage python knn.py -mode [...]'
    print 'Mode is either bl_random for baseline random test,', \
          'bl_popular for the baseline most popular statistics,', \
          '-knn for the baseline prec at 10 using knn,', \
          '-user for a user query, or -artist for an artist query.'
    print 'KNN Precision at 10 query usage: python knn.py -knn k weighted? sim_metric'
    print ''
    print 'User Query usage: python knn.py -user user_id k weighted? sim_metric'
    print ''
    print 'Artist Query usage: python knn.py -artist artist_name k weighted? sim_metric'
    print ''
    print 'k = number of nearest neighbors to use'
    print 'weighted = 0 to use non-weighted, 1 for anything else'
    print 'sim_metric = 0 for inverse euclidean, 1 for dot product, 2 for cosine'
    quit()
if len(sys.argv) == 1:
    print_usage_and_quit()


modes = ['-bl_random', '-bl_popular', '-user', '-artist', '-knn']
mode = sys.argv[1].lower()
if mode not in modes:
    print "Invalid mode!"
    print_usage_and_quit()

if mode == modes[0]:
    baseline_random(training, test)
elif mode == modes[1]:
    baseline_most_popular(training, test)
elif mode == modes[4]:
    if len(sys.argv) < 5:
        print 'Too few arguments!'
        print_usage_and_quit()

    k = int(sys.argv[2])
    weighted = sys.argv[3]
    weighted = False if weighted == '0' else True
    weighted_str = "weighted" if weighted else "non-weighted"
    sim_metric = sys.argv[4]

    if sim_metric == '0':
        sim_func = inverse_euclidean
        sim_func_str = "inverse euclidean"
    elif sim_metric == '1':
        sim_func = dot_product
        sim_func_str = "dot product"
    elif sim_metric == '2':
        sim_func = cos
        sim_func_str = "cosine"
    else:
        print 'Invalid similarity metric flag'
        print_usage_and_quit()

    prec_at_10 = baseline_knn(training, test, k, sim_func, weighted)
    print 'Calculating precision @ 10 for k = ', k, weighted_str, \
           sim_func_str, 'similarity'
    print prec_at_10

else:
    if len(sys.argv) < 6:
        print 'Too few arguments!'
        print_usage_and_quit()

    k = int(sys.argv[3])
    weighted = sys.argv[4]
    weighted = False if weighted == '0' else True
    sim_metric = sys.argv[5]

    if sim_metric == '0':
        sim_func = inverse_euclidean
    elif sim_metric == '1':
        sim_func = dot_product
    elif sim_metric == '2':
        sim_func = cos
    else:
        print 'Invalid similarity metric flag'
        print_usage_and_quit()

    if mode == '-user':
        user_id = int(sys.argv[2])
        user_query(training, user_id, k, sim_func, weighted)

