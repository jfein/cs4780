from tree import Node, Leaf

def gen_tree(data):
    # Validate input
    if len(data) == 0:
        raise Exception("Generating tree on empty data set")

    # Base case if everything in data is same location
    locs = zip(*data)[1]
    if len(set(locs)) == 1:
        return Leaf(locs[0])
    
    # Recursive case
    split_wifi_id , split_wifi_strength , data_l , data_r = split_finder(data)
    return Node(split_wifi_id , split_wifi_strength , gen_tree(data_l) , gen_tree(data_r))