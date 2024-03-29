import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Defines the scope of access
scope = 'user-library-read playlist-modify-public playlist-modify-private'

# Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id="c5a2800cd23e42b39e5097be1ec1602b",
                                               client_secret="707ec947cb8a49c5b2187229850b461a",
                                               redirect_uri="http://localhost:8888/callback"))

# Defines filters
limit = 10
market = "US"
seed_genres = "indie"
target_danceability = 0.9
seed_artists = '0XNa1vTidXlvJ2gHSsRi4A'
seed_tracks = '55SfSsxneljXOk5S3NVZIW'

# Gets recommendations
results = sp.recommendations(seed_artists=[seed_artists], seed_genres=[seed_genres],
                             seed_tracks=[seed_tracks], limit=limit,
                             target_danceability=target_danceability, market=market)

# Creates a new playlist
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user_id, "NAME YOUR PLAYLIST HERE", public=False)

# Extracts the track URIs
track_uris = [track['uri'] for track in results['tracks']]

# Adds tracks to the new playlist
sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

# Outputs the result
print(f"Your playlist is ready at {playlist['external_urls']['spotify']}")