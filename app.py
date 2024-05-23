# app.py
from flask import Flask, request, redirect, session, url_for, render_template
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from playlistcreator import create_playlist_with_filters
import random


# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Spotify OAuth setup
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='playlist-modify-public user-read-private',
    cache_path='.spotify_cache'
)

@app.route('/')
def index():
    # Check if user is logged in by looking for token info in session
    user_logged_in = 'token_info' in session

    # Render the index page, passing login status to template
    return render_template('index.html', user_logged_in=user_logged_in)

@app.route('/login')
def login():
    # Get Spotify auth URL and redirect user to Spotify login page
    auth_url = sp_oauth.get_authorize_url()
    auth_url_with_show_dialog = auth_url + "&show_dialog=true"

    return redirect(auth_url_with_show_dialog)

@app.route('/callback')
def callback():
    # Handle callback from Spotify OAuth flow, retrieving access token
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code, as_dict=True)

    # Store token info in session for later use
    session['token_info'] = token_info

    # Redirect user back to the index page after login
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Clear session to log user out
    session.clear()

    # Redirect user back to the index page after logout
    return redirect(url_for('index'))

def get_spotify_client():
    # Retrieve Spotify client with user's access token
    token_info = session.get('token_info', None)

    # Refresh token if expired and update session
    if not token_info or sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Return authenticated Spotify client
    return sp

@app.route('/generate_playlist', methods=['GET', 'POST'])
def generate_playlist():
    # Predefined list of top genres for selection in the form
    top_genres = ["pop", "rock", "hip-hop", "dance", "electronic", "indie", "classical", "jazz", "metal", "country",
                  "folk", "blues", "funk", "r&b", "reggae", "soul", "punk", "disco", "house", "techno"]

    if request.method == 'POST':
        # Process form data to generate playlist
        playlist_name = request.form.get('playlist_name', "My Spotify Playlist")
        limit = request.form.get('limit', 10, type=int)
        seed_genres = request.form.get('seed_genres')  # Retrieve the selected genre

        if seed_genres == 'random':
            # Randomly selects a genre from the list
            seed_genres = random.choice(top_genres)

        # Collect feature values if their respective checkbox is checked
        features = {}
        for feature_name in ['danceability', 'energy', 'acousticness', 'speechiness', 'liveness', 'loudness']:
            checkbox_name = f"enable_{feature_name}"
            if checkbox_name in request.form:  # This checks if the checkbox was checked
                feature_value = request.form.get(f"target_{feature_name}", type=float)
                features[f"target_{feature_name}"] = feature_value

        try:
            sp = get_spotify_client()
            # Passing features dictionary directly
            playlist_url = create_playlist_with_filters(sp, name=playlist_name, limit=limit, seed_genres=seed_genres,
                                                        public=True, **features)
            session['playlist_url'] = playlist_url  # Stores playlist URL in the session
            return redirect(url_for('playlist_created'))  # Redirects to confirmation page
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return render_template('error.html', error_message=str(e))

    return render_template('generate.html', top_genres=top_genres)


@app.route('/playlist_created')
def playlist_created():
    # Retrieve and display the created playlist URL from session
    playlist_url = session.get('playlist_url', '#')  # Retrieves playlist URL from the session
    return render_template('playlist_created.html', playlist_url=playlist_url)


if __name__ == '__main__':
    app.run(debug=True, port=8888)
