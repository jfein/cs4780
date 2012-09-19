from tree import Node, Leaf
from split_finder import split_finder
from util import load_training

def gen_tree(data):
    print "LEN DATA: {0}".format(len(data))
    
    if len(data) == 2:
        print "{0}".format(data)
    
    # Validate input
    if len(data) == 0:
        raise Exception("Generating tree on empty data set")

    # Base case if everything in data is same location
    locs = zip(*data)[1]
    if len(set(locs)) == 1:
        print "\tFOUND A LEAF!"
        return Leaf(locs[0])
    
    # Recursive case
    split_wifi_id , split_wifi_strength , data_l , data_r = split_finder(data)
    print "\t\tleft:{0} - right:{1}".format(len(data_l), len(data_r))
    return Node(split_wifi_id , split_wifi_strength , gen_tree(data_l) , gen_tree(data_r))
    
    
def classify(node, point):
    if type(node) == List:
        return node.location
        
    if point[node.split_wifi_id] <= node.split_wifi_strength:
        return classify(node.left_node, point)
    else:
        return classify(node.right_node, point)
        

def test_accuracy(root, data):
    wrong = {}
    total = {}
    for point, location in data:
        total[location] += 1.0
        if classify(root, point) != location:
            wrong[location] += 1.0
    
    err_locs = dict( (n, wrong.get(n, 0) / total.get(n, 0)) for n in set(wrong)|set(total) )
    err_all = sum(wrong.values()) / sum(total.values())
    return (err_locs , err_all)
    


data = load_training()

root = gen_tree(data)

err_locs, err_all = test_accuracy(root, data)

print err_locs
print err_all