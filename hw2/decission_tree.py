from split_finder import split_finder
from collections import Counter


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
    # Validate input
    if len(data) == 0:
        raise Exception("Generating tree on empty data set")

    # Base case if everything in data is same location
    locs = zip(*data)[1]
    if len(set(locs)) == 1:
        return Leaf(locs[0])

    # Recursive case
    split_wifi_id , split_wifi_strength , data_l , data_r = split_finder(data)

    # If we have a child with 0 data, make this a leaf instead
    if len(data_l) == 0 or len(data_r) == 0:
        return Leaf(Counter(zip(*(data_l + data_r))[1]).most_common(1)[0][0])

    return Node(split_wifi_id , split_wifi_strength , gen_tree(data_l) , gen_tree(data_r))


def classify(node, point):
    if isinstance(node, Leaf):
        return node.location

    if point.get(node.split_wifi_id, float("-inf")) <= node.split_wifi_strength:
        return classify(node.left_node, point)
    else:
        return classify(node.right_node, point)

def count_occurences(root):
    '''
    Returns a map of {location : count} which represents
    how many leaves of this tree have that location
    '''
    if isinstance(root, Leaf):
        return {root.location : 1}
    else:
        occurences = {}
        for loc, count in count_occurences(root.left_node):
            occurences[loc] = occurences.get(loc, 0) + count
        for loc, count in count_occurences(root.right_node):
            occurences[loc] = occurences.get(loc, 0) + count
        return occurences

