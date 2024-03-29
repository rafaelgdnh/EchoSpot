import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time, random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve client ID and secret from environment variables
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

playlist_uri = 'spotify:playlist:1RTENWq73MEx1Pop40ZZ5S'

# Function to handle pagination and fetch all tracks from playlists
def get_playlist_tracks(playlist_id):
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Fetch tracks from playlist
tracks = get_playlist_tracks(playlist_uri)

# Creates DataFrame to store the features
df_columns = ['track_id', 'energy', 'loudness', 'speechiness', 'valence', 'liveness',
              'tempo', 'danceability', 'acousticness', 'duration_ms', 'instrumentalness',
              'popularity', 'market']
df = pd.DataFrame(columns=df_columns)

# Retrieves audio features for each track and stores in a DataFrame
for track in tracks:
    track_id = track['track']['id']
    features = sp.audio_features(track_id)[0]
    if features:
        df = df._append({
            'track_id': track_id,
            'energy': features['energy'],
            'loudness': features['loudness'],
            'speechiness': features['speechiness'],
            'valence': features['valence'],
            'liveness': features['liveness'],
            'tempo': features['tempo'],
            'danceability': features['danceability'],
            'acousticness': features['acousticness'],
            'duration_ms': features['duration_ms'],
            'instrumentalness': features['instrumentalness'],
            'popularity': track['track']['popularity'],
            'market': track['track']['available_markets']
        }, ignore_index=True)
    time.sleep(random.uniform(3, 6))  # To avoid rate limits

print(df)

df.to_csv('/Users/rafaelgodinho/DataspellProjects/EchoSpot/top500songs.csv')



