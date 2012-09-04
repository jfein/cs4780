'''
Created on Sep 4, 2012

@author: Will
'''

def load_song_data(filename):
    f = open(filename, 'r')
    song_data = {}
    for song_datum in f:
        id, title, artist = song_datum.split("\t")
        song_data[id] = (title, artist)

    return song_data

def parse_training(filename):
    '''
    Returns a list of all training data. 
    Training data is represented as a map
    from uid to song_map, where uid is
    the user id and song_map is a dictionary 
    that maps song ids to the number of times the song
    has been played. If a song id is not in the
    song_map then we assume the song has been 
    played 0 times.
    '''

    f = open(filename, 'r')
    examples = {}
    for example in f:
        uid, songs = [x.strip() for x in example.split('-')]
        uid = int(uid)
        song_map = {}
        for song in songs.split(" "):
            id, plays = [int(x) for x in song.split(":")]
            song_map[id] = plays

        examples[uid] = song_map

    return examples


def parse_test(filename):
    '''
    Parses test file. Returns a map of
    user_id -> list of omitted songs
    '''
    f = open(filename, 'r')
    examples = {}
    for example in f:
        uid, songs = [x.strip() for x in example.split('-')]
        uid = int(uid)
        songs = [int(x) for x in songs.split(' ')]
        examples[uid] = songs

    return examples
