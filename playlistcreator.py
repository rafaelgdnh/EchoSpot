def create_playlist_with_filters(sp, name="My Custom Playlist", limit=10, target_danceability=0.5, target_energy=0.5,
                                 target_acousticness=0.5, target_speechiness=0.5, target_liveness= 0.5,
                                 target_loudness=-30,
                                 seed_genres="indie", seed_artists=None, seed_tracks=None, public=False, features=None):
    # Ensure at least one seed value is provided
    if not seed_artists and not seed_tracks and not seed_genres:
        raise ValueError("At least one seed value (artist, track, or genre) must be provided.")

    if features is None:
        features = {}


    # Prepare the payload for the recommendations request
    # Only include features that were checked by the user
    recommendation_args = {
        "limit": limit,
    }

    # Dynamically add features that are enabled by the user
    for feature, value in features.items():
        if value['enabled']:  # Check if the feature is enabled
            recommendation_args[feature] = value['value']

    # Get recommendations
    results = sp.recommendations(seed_artists=[seed_artists] if seed_artists else [],
                                 seed_genres=[seed_genres] if seed_genres else [],
                                 seed_tracks=[seed_tracks] if seed_tracks else [],
                                 limit=limit, target_danceability=target_danceability, target_energy=target_energy,
                                 target_acousticness=target_acousticness, target_speechiness=target_speechiness,
                                 target_liveness=target_liveness, target_loudness=target_loudness,
                                 market="US")  # Consider dynamically setting or omitting the market

    # Creates a new playlist for the current user
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user_id, name, public=public)

    # Extracts the track URIs and add them to the new playlist
    track_uris = [track['uri'] for track in results['tracks']]
    sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)

    # Returns the playlist URL
    return playlist['external_urls']['spotify']

