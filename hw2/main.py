from decission_tree import gen_tree, classify
from util import load_training


def test_accuracy(root, data, prune=-1):
    wrong = {}
    total = {}
    
    for point, location in data:
        total[location] = total.get(location, 0) + 1.0
        if classify(root, point, prune) != location:
            wrong[location] = wrong.get(location, 0) + 1.0
    
    err_locs = dict( (n, wrong.get(n, 0) / total.get(n, 0)) for n in set(wrong)|set(total) )
    err_all = sum(wrong.values()) / sum(total.values())
    return (err_locs , err_all)
    
    
def test_accuracy_compare(root, data, prune1, prune2):
    d1 = 0
    d2 = 0

    for point, location in data:
        h1_right = classify(root, point, prune1) == location
        h2_right = classify(root, point, prune2) == location
        
        if h1_right and not h2_right:
            d1 += 1
        if h2_right and not h1_right:
            d2 += 1
    
    return (d1, d2)
    

    
training_data = load_training("wifi.train")
test_data = load_training("wifi.test")

root = gen_tree(training_data)

print "\n"

err_locs, err_all = test_accuracy(root, training_data)
print "TEST ACCURACY ON TRAINING SET:"
print "\tLOCATION SPECIFIC ERRORS:"
for loc, val in err_locs.iteritems():
    print "\t\t{0} : {1}".format(loc,val)
print "\tOVERALL ERROR:\n\t\t{0}".format(err_all)

print "\n"

err_locs, err_all = test_accuracy(root, test_data)
print "TEST ACCURACY ON TEST SET:"
print "\tLOCATION SPECIFIC ERRORS:"
for loc, val in err_locs.iteritems():
    print "\t\t{0} : {1}".format(loc,val)
print "\tOVERALL ERROR:\n\t\t{0}".format(err_all)

print "\n"

err_locs, err_all = test_accuracy(root, test_data, 2)
print "TEST ACCURACY ON TEST SET AND PRUNING AT 2:"
print "\tLOCATION SPECIFIC ERRORS:"
for loc, val in err_locs.iteritems():
    print "\t\t{0} : {1}".format(loc,val)
print "\tOVERALL ERROR:\n\t\t{0}".format(err_all)

print "\n"

d1, d2 = test_accuracy_compare(root, test_data, -1, 2)
print "COMPARE NO PRUNE AND PRUNE 2:"
print "\tD1: {0}\n\tD2: {1}".format(d1, d2)