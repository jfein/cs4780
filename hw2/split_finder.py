import math
import parser

def split_finder(sample_set):
    '''
    Sample set is a list of
    (signal_map, location)
    and return
    (signal_id, signal_strength, left_subset, right_subset)
    '''
    sample_size = float(len(sample_set))

    all_signal_ids = set()
    all_signal_strengths = set()

    # Place holders for the best splits that we've found so far
    min_entropy = float("inf")
    signal_id_split = None
    signal_strength_split = None
    left_subset_split = None
    right_subset_split = None

    signal_maps, _ = zip(*sample_set)
    for signal_map in signal_maps:
        all_signal_ids.update(signal_map.keys())
        all_signal_strengths.update(signal_map.values())

    for potential_signal_id in all_signal_ids:
        for potential_signal_strength in all_signal_strengths:

            # Partition into <= potential_signal_strength and > potential_signal_strength
            left_subset, right_subset = [], []

            for signal_map, location in sample_set:
                strength = signal_map.get(potential_signal_id, -10000)
                if(strength <= potential_signal_strength):
                    left_subset.append((signal_map, location))
                else:
                    right_subset.append((signal_map, location))

            entropy = (len(left_subset) / sample_size) * calculate_entropy(left_subset) + \
                      (len(right_subset) / sample_size) * calculate_entropy(right_subset)

            if entropy < min_entropy:
                min_entropy = entropy
                signal_id_split = potential_signal_id
                signal_strength_split = potential_signal_strength
                left_subset_split = left_subset
                right_subset_split = right_subset

    if min_entropy == float("inf") or signal_id_split is None or \
        signal_strength_split is None or left_subset_split is None:
        raise Exception("Min entropy/signal id split/signal strength split not set correctly")

    return signal_id_split, signal_strength_split, left_subset_split, right_subset_split


def calculate_entropy(sample_set):
    '''
    Sample set is a list of (signal_map, location)
    '''
    location_count = {}
    total_locations = float(len(sample_set))

    for _, location in sample_set:
        location_count[location] = location_count.get(location, 0) + 1

    entropy = 0.0
    for location, num_appeared in location_count.iteritems():
        location_prob = num_appeared / total_locations
        entropy += -1.0 * location_prob * math.log(location_prob, 2)

    return entropy



