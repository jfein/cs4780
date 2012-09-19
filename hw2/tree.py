
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