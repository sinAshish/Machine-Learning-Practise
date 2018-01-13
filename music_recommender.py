import os
from scipy.sparse import coo_matrix
print os.getcwd()

def no_file():
    print 'Dataset not found, please download the file from:'
    print 'http://mtg.upf.edu/static/datasets/last.fm/lastfm-dataset-360K.tar.gz (1.6GB)'
    print 'then place it in recommender_system_py/data/ and change the file_path'
    print 'variable on the fetch_lastfm function'


def fetch_lastfm(min_plays=200):
   
    file_path = 'last_fm_data.tsv'

    if not os.path.exists(file_path):
        return no_file()

    # Data to create our coo_matrix
    data, row, col = [], [], []

    # Artists by id, and users
    artists, users = {}, {}

    # Read the file and fill variables with data to
    # create the matrix and have the artists by id
    with open(file_path) as data_file:
        for n, line in enumerate(data_file):

            # If you use the original data from lastfm (14 million lines)
            # if n == SOMEINT: break
            
            # Readable data (for humans)
            readable_data = line.split('\t')
            user =           readable_data[0]
            artist_id =      readable_data[1]
            artist_name =    readable_data[2]
            plays =     int(readable_data[3])

            if user not in users:
                users[user] = len(users)

            if artist_id not in artists:
                artists[artist_id] = {
                        'name' : artist_name,
                        'id' : len(artists)
                        }

            # Data for the coo_matrix if the artist was played > 200 times
            if plays > min_plays:
                data.append(plays)
                row.append(users[user])
                col.append(artists[artist_id]['id'])

    # Our matrix: ((plays, (user, artist)))
    coo = coo_matrix((data,(row,col)))

    # We return the matrix, the artist dictionary and the amount of users
    dictionary = {
        'matrix' : coo,
        'artists' : artists,
        'users' : len(users)
    }

    return dictionary


import numpy as np
from lightfm import LightFM



data = fetch_lastfm()

model = LightFM(loss='warp')
model.fit(data['matrix'], epochs=30, num_threads=2)

# Get recommendationns function
def get_recommendations(model, coo_mtrx, users_ids):

    n_items = coo_mtrx.shape[1]

    for user in users_ids:

        # TODO create known positives
        # Artists the model predicts they will like
        scores = model.predict(user, np.arange(n_items))
        top_scores = np.argsort(-scores)[:3]

        print 'Recomendations for user %s:' % user

        for x in top_scores.tolist():
            for artist, values in data['artists'].iteritems():
                if int(x) == values['id']:
                    print '   - %s' % values['name']

        print '\n' # Get it pretty


user_1 = raw_input('Select user_1 (0 to %s): ' % data['users'])
user_2 = raw_input('Select user_2 (0 to %s): ' % data['users'])
user_3 = raw_input('Select user_3 (0 to %s): ' % data['users'])
print '\n' # Get it pretty

get_recommendations(model, data['matrix'], [user_1, user_2, user_3])
