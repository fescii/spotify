import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
from .sorters import bubble_sort, quick_sort


class SpotifyAnalyzer:
    """
    A class for analyzing Spotify music data and creating mood-based playlists.

    Features:
    - Authentication with Spotify API
    - Retrieval of track audio features
    - Mood-based playlist generation
    - Advanced sorting and filtering capabilities

    Attributes:
        client_id (str): Spotify API client ID
        client_secret (str): Spotify API client secret
        sp (spotipy.Spotify): Authenticated Spotify client instance
    """

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        """
        Initialize Spotify client with authentication
        If client_id, client_secret, and redirect_uri are not provided, they are loaded from .env file.
        """

        if client_id and client_secret and redirect_uri:
            self.client_id = client_id
            self.client_secret = client_secret
            self.redirect_uri = redirect_uri
        else:
            # Load from environment variables if not provided
            load_dotenv()
            self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
            self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
            self.redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

        if not self.client_id or not self.client_secret or not self.redirect_uri:
            raise ValueError(
                "Missing Spotify credentials. Please provide client_id , client_secret, and redirect_uri "
                "either as parameters or in a .env file."
            )

        # Initialize Spotify client with auth manager
        try:
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    redirect_uri=redirect_uri,
                    scope="user-library-read playlist-modify-public user-top-read",
                )
            )
            # Test the connection
            self.sp.current_user()
            print("Successfully connected to Spotify!")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Spotify: {str(e)}")

    def analyze_artist_albums(self, artist_id: str) -> pd.DataFrame:
        """
        Analyze all albums from a specific artist and sort them by energy/mood.

        Args:
            artist_id (str): Spotify artist ID

        Returns:
            pd.DataFrame: DataFrame containing album analysis
        """
        # Get all albums from the artist
        albums = self.sp.artist_albums(artist_id, album_type="album")

        albums_data = []
        for album in albums["items"]:
            # Get all tracks from album
            tracks = self.sp.album_tracks(album["id"])
            track_ids = [track["id"] for track in tracks["items"]]

            # Get audio features for all tracks
            features = self.get_track_features(track_ids)

            # Calculate average features for the album
            avg_features = {
                "energy": sum(f["energy"] for f in features if f) / len(features),
                "valence": sum(f["valence"] for f in features if f) / len(features),
                "danceability": sum(f["danceability"] for f in features if f)
                / len(features),
            }

            albums_data.append(
                {
                    "name": album["name"],
                    "release_date": album["release_date"],
                    **avg_features,
                }
            )

        return pd.DataFrame(albums_data)

    def recommend_similar_tracks(
        self, seed_tracks: List[str], limit: int = 20
    ) -> pd.DataFrame:
        """
        Get track recommendations based on seed tracks and sort by similarity.

        Args:
            seed_tracks (List[str]): List of track IDs to base recommendations on
            limit (int): Number of recommendations to return

        Returns:
            pd.DataFrame: DataFrame containing recommended tracks
        """
        recommendations = self.sp.recommendations(seed_tracks=seed_tracks, limit=limit)
        track_ids = [track["id"] for track in recommendations["tracks"]]
        features = self.get_track_features(track_ids)

        return self.merge_track_info(recommendations["tracks"], features)

    def get_track_features(self, track_ids: List[str]) -> List[Dict]:
        """Get audio features for multiple tracks"""
        features = []
        # Process in batches of 100 (Spotify API limit)
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i : i + 100]
            features.extend(self.sp.audio_features(batch))
        return features

    def merge_track_info(
        self, tracks: List[Dict], features: List[Dict]
    ) -> pd.DataFrame:
        """Merge track information with their audio features"""
        track_data = []

        for track, feature in zip(tracks, features):
            if feature is None:
                continue

            track_info = {
                "id": track["id"],
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "popularity": track["popularity"],
                "duration_ms": track["duration_ms"],
                "release_date": track["album"]["release_date"],
                "danceability": feature["danceability"],
                "energy": feature["energy"],
                "valence": feature["valence"],
                "tempo": feature["tempo"],
            }
            track_data.append(track_info)

        return pd.DataFrame(track_data)

    def create_mood_playlist(self, mood: str, limit: int = 50) -> pd.DataFrame:
        """Create a playlist based on mood using audio features"""
        # Get user's top tracks
        top_tracks = self.sp.current_user_top_tracks(
            limit=limit, time_range="medium_term"
        )
        track_ids = [track["id"] for track in top_tracks["items"]]

        # Get audio features
        features = self.get_track_features(track_ids)
        df = self.merge_track_info(top_tracks["items"], features)

        # Define mood parameters
        mood_params = {
            "happy": {"valence": 0.7, "energy": 0.7},
            "sad": {"valence": 0.3, "energy": 0.3},
            "energetic": {"energy": 0.8, "tempo": 120},
            "chill": {"energy": 0.3, "tempo": 100},
        }

        # Filter and sort based on mood
        if mood in mood_params:
            for feature, target in mood_params[mood].items():
                df[f"{feature}_distance"] = abs(df[feature] - target)

            df["mood_score"] = df[
                [f"{feature}_distance" for feature in mood_params[mood].keys()]
            ].mean(axis=1)
            return df.sort_values("mood_score")

        return df

    def get_top_artist_id(self) -> str:
        """Get the Spotify ID of the user's top artist"""
        top_artists = self.sp.current_user_top_artists(limit=1)
        return top_artists["items"][0]["id"] if top_artists["items"] else None

    def get_audio_features_data(self, playlist) -> Dict[str, float]:
        """Get average audio features for the playlist"""
        features = self.get_track_features(
            [track["id"] for track in playlist.to_dict("records")]
        )
        if not features:
            return {}

        # Calculate average of each feature
        avg_features = {
            "energy": sum(f["energy"] for f in features if f) / len(features),
            "valence": sum(f["valence"] for f in features if f) / len(features),
            "danceability": sum(f["danceability"] for f in features if f)
            / len(features),
        }
        return avg_features

    def get_genre_distribution_data(self, tracks_list) -> Dict[str, int]:
        """Get genre distribution data optimized for fewer API calls"""
        artist_ids = {
            track["artists"][0]["id"]
            for track in tracks_list
            if "artists" in track and track["artists"]
        }
        genres = []

        # Fetch artist info in batches to reduce API calls
        for i in range(0, len(artist_ids), 50):
            batch = list(artist_ids)[i : i + 50]
            artists_info = self.sp.artists(batch)
            for artist in artists_info["artists"]:
                genres.extend(artist.get("genres", []))

        # Count the genres and return top 10
        genre_counts = pd.Series(genres).value_counts().head(10)
        return genre_counts.to_dict()

    def get_top_songs_data(self, tracks_list) -> List[Dict[str, Any]]:
        """Get data for the top songs visualization"""
        return [
            {
                "name": track["name"],
                "artist": track["artists"][0]["name"],
                "popularity": track["popularity"],
            }
            for track in tracks_list
        ]
