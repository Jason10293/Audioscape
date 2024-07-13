import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
import json
from sklearn.preprocessing import MinMaxScaler
from dateutil.relativedelta import relativedelta
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def generate_recommendations(playlist_id):
    load_dotenv('API_keys.env')

    # with open('user_playlists.json', 'r') as infile:
    #     playlists = json.load(infile)

    # for item in playlists['items']:
    #     print(item['id'])

    # Initialize the Spotify client with OAuth for accessing user library
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('CLIENT_ID'),
                                                client_secret=os.environ.get('CLIENT_SECRET'),
                                                redirect_uri=os.environ.get('REDIRECT_URI'),
                                                scope="user-library-read"))



    def feature_engineer(df):
        scaler = MinMaxScaler()
        
        features_to_scale = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
        features_to_OHE = ['key', 'explicit', 'popularity']
        
        tfidf = TfidfVectorizer()

        #tfidf cannot handle null values
        df['track_genre'] = df['track_genre'].ffill()
        tfidf_matrix = tfidf.fit_transform(df['track_genre'])
        
        genre_df = pd.DataFrame(tfidf_matrix.toarray())
        genre_df.columns = ['genre_' + i for i in tfidf.get_feature_names_out()]
        # Reset index of genre_df to allow for clean concatenation later
        genre_df.reset_index(drop = True, inplace=True)

        #scale numerical features
        df[features_to_scale] = scaler.fit_transform(df[features_to_scale])
        
        def perform_OHE(df, column):
            OHE = pd.get_dummies(df[column], drop_first=True, dtype=int, prefix=column)
            df = df.drop(columns=column, axis='columns')
            df = pd.concat([df, OHE], axis=1)
            return df

        #Seperate popularity into 20 buckets -> OHE the popularity
        df['popularity'] = df['popularity'].apply(lambda x: x//5)

        for feature in features_to_OHE:
            df = perform_OHE(df, feature)

        #Combine the main df and the genre_df from the tfidf
        df = pd.concat([df, genre_df], axis=1)
        df = df.drop(columns=['track_genre'], axis = 'columns')
        return df



    df = pd.read_csv('Server/dataset.csv')
    df = df[df.columns[1:]]
    df = df.drop(columns=['time_signature', 'duration_ms'])

    playlist_length = 0
    count = 0
    playlist_items = []
    while True:
        response = sp.playlist_items(playlist_id, offset = 100 * count)
        tracks = response['items']
        if not tracks:
            break
        playlist_items.extend(tracks)
        count += 1

    for i in range(len(playlist_items)):
        if playlist_items[i]['track'] is not None:
            playlist_length += 1
    

    track_ids = []
    date_added = {} #Tracks when a song was added to a playlist

    #sp.playlist_track has a limit of 100 items per API call
    for i in range(0, playlist_length, 100):
        playlist = sp.playlist_tracks(playlist_id, market = 'CAN',fields='items', limit=100, offset = i)
        #playlist[items] has information on all the tracks in the playlist
        for index, track in enumerate(playlist['items']):
            if track['track'] is not None and track['track']['id'] is not None:
                date_added[track['track']['id']] = playlist['items'][index]['added_at']
                track_ids.append(track['track']['id'])
            else:
                print(track['track'])
        

    artist_genres = {}
    playlist_track_audio_features = []
    #
    for i in range(0,len(track_ids), 100):
        playlist_track_audio_features.extend(sp.audio_features(track_ids[i : i + 100]))

    playlist_track_info = []
    for i in range(0, len(track_ids), 50):
        playlist_track_info.extend(sp.tracks(track_ids[i : i + 50])['tracks'])


    track_audio_features = [audio_feature for audio_feature in playlist_track_audio_features]
    track_info = [info for info in playlist_track_info]
    track_artist_ids = [info['artists'][0]['id'] for info in playlist_track_info]


    for i in range(0, len(track_artist_ids), 50):
        results = sp.artists(track_artist_ids[i: i + 50])
        for artist in results['artists']:
            #Only get the first (main) genre from an artist as artist's have multiple genres
            artist_genres[artist['name']] = artist_genres.get(artist['name'], artist['genres'][0] if artist['genres'] else None)

    for index ,id in enumerate(track_ids):
        track_artists = [artist['name'] for artist in track_info[index]['artists']]
        main_artist_genre = artist_genres[track_artists[0]]
        audio_features_keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        audio_data = {
            'track_id': id,
            'artists': ';'.join(track_artists),
            'album_name': track_info[index]['album']['name'],
            'track_name': track_info[index]['name'],
            'popularity': track_info[index]['popularity'],
            'explicit': track_info[index]['explicit'],
            **{key: track_audio_features[index][key] for key in audio_features_keys},
            'track_genre': main_artist_genre
        }
        df.loc[len(df.index)] = audio_data

    df = feature_engineer(df)

    #Bug here
    track_data = df.tail(playlist_length).copy()
    df = df.iloc[:-playlist_length]
    track_data['date_added'] = date_added.values()

    # Assuming track_data is already defined and feature_engineered
    track_data = pd.DataFrame(track_data)
    track_data['date_added'] = pd.to_datetime(track_data['date_added']).dt.date
    first_date = track_data.iloc[0]['date_added']

    # Calculate weights using linear descent
    weights = []
    for index, row in track_data.iterrows():
        months_difference = relativedelta(row['date_added'], first_date).months
        # Linear descent weighting
        weights.append(round(1/(months_difference + 1), 3))

    track_data['weight'] = weights
    track_data = track_data.drop(columns=['date_added'])

    num_rows = len(track_data.values)
    num_cols = len(track_data.columns)
    results_array = [0] * (num_cols - 5)
    for i in range(num_rows):
        row = track_data.iloc[i]
        row_weight = track_data.iloc[i, -1]
        for index, value in enumerate(row[4:-1]):
            results_array[index] += value * row_weight


    vectors = df.iloc[:, 4:].values
    input_vector = np.array(results_array)
    similarity_matrix = cosine_similarity(input_vector.reshape(1,-1), vectors)

    similarity_array = similarity_matrix.flatten()

    top_20_songs = set()
    counter = 0
    while len(top_20_songs) < 20:
        ith_most_similar_index = similarity_array.argsort()[::-1][counter]
        track_name = df.iloc[ith_most_similar_index]['track_name']
        artist = df.iloc[ith_most_similar_index]['artists']
        top_20_songs.add(track_name + " | " + artist)
        counter += 1

    for track in top_20_songs:
        print(track)

generate_recommendations('2zx3OZLsEhIcPZ5cmH9WtS')