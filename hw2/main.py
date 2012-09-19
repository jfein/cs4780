from decission_tree import gen_tree, classify
from util import load_training


def test_accuracy(root, data):
    wrong = {}
    total = {}
    
    for point, location in data:
        total[location] = total.get(location, 0) + 1.0
        if classify(root, point) != location:
            wrong[location] = wrong.get(location, 0) + 1.0
    
    err_locs = dict( (n, wrong.get(n, 0) / total.get(n, 0)) for n in set(wrong)|set(total) )
    err_all = sum(wrong.values()) / sum(total.values())
    return (err_locs , err_all)
    

    
training_data = load_training("wifi.train")
test_data = load_training("wifi.test")

root = gen_tree(training_data)

err_locs, err_all = test_accuracy(root, training_data)
print "TEST ACCURACY ON TRAINING SET:\n"
print "LOCATION SPECIFIC ERRORS:\n{0}\n".format(err_locs)
print "OVERALL ERROR:\n{0}".format(err_all)

print "\n"

err_locs, err_all = test_accuracy(root, test_data)
print "TEST ACCURACY ON TRAINING SET:\n"
print "LOCATION SPECIFIC ERRORS:\n{0}\n".format(err_locs)
print "OVERALL ERROR:\n{0}".format(err_all)