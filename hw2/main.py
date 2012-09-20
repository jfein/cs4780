import random
from decission_tree import gen_tree, classify, max_depth
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
    
    
def cross_validate(fold, data):
    def make_chunks(seq, num_chunks):
        avg = len(seq) / float(num_chunks)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out
        
    random.shuffle(data)
    chunks = make_chunks(data, fold)

    total_err = 0
    total_err_prune = 0
    for i in range(fold):
        test_data = chunks[i]
        train_data = chunks[:i] + chunks[i+1:]
        
        root = gen_tree(training_data)
        
        total_err += test_accuracy(root, test_data)[1]
        total_err_prune += test_accuracy(root, test_data, 2)[1]
        
    return (total_err / fold , total_err_prune / fold)
    

def validation_error(test_data, train_data_orig, validate_ratio):
    random.shuffle(train_data_orig)
    
    # Make validation set
    split = int(len(train_data_orig) * validate_ratio)
    validate_data = train_data_orig[:split]
    train_data = train_data_orig[split:]
    
    # Initial tree
    root = gen_tree(train_data)
    
    # Find best pruning
    least_err = float("inf")
    best_prune = -1
    for i in range(max_depth(root)):
        err = test_accuracy(root, validate_data, i)[1]
        if err < least_err:
            least_err = err
            best_prune = i
    
    # Return err of best pruning against test data
    return test_accuracy(root, test_data, best_prune)[1]
            

            
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

print "\n"

err , err_prune = cross_validate(10, training_data + test_data)
print "CROSS VALIDATE 10-FOLD AVERAGE ERRORS:"
print "\tNO PRUNING:\t{0}".format(err)
print "\tPRUNE 2:\t{0}".format(err_prune)

print "\n"

print "VALIDATION SET TESTING:"
for ratio in map(lambda x: x/10.0, range(1, 10)):
    for i in range(100):
        err = validation_error(test_data, training_data, ratio)
        print "\t{0:f} : {1:f}".format(ratio, err)