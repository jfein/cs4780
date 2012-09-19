from split_finder import split_finder


class Node:
    def __init__(
            self,
            split_wifi_id,
            split_wifi_strength,
            left_node, 
            right_node):
        self.split_wifi_id = split_wifi_id
        self.split_wifi_strength = split_wifi_strength
        self.left_node = left_node
        self.right_node = right_node
		
		
class Leaf:
    def __init__(
            self,
            location):
        self.location = location


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
