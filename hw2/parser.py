'''
Created on Sep 17, 2012

@author: Will
'''
import re
TRAINING_FILE_NAME = "wifi.train"
TEST_FILE_NAME = "wifi.test"

def load_training():
    '''
    Load the training data and return it as a list of
    (signal_map, location) tuples, where signal_map is a 
    map from
    '''
    training_file = open(TRAINING_FILE_NAME, 'r')

    signal_pattern = re.compile(r'\d:\s?-\d{1,2}')
    location_pattern = re.compile(r'[A-Z]+_?\d?')

    training = []
    for line in training_file:
        location_match = location_pattern.search(line)
        if not location_match:
            print "NO LOCATION MATCH", line

        location = location_match.group()
        signal_map = {}
        for signal in signal_pattern.findall(line):
            station, station_strength = [int(x) for x in signal.split(":")]
            signal_map[station] = station_strength

        training.append((signal_map, location))

    return training

load_training()
