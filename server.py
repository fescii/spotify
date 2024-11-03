from flask import Flask, jsonify, request, send_from_directory
from src.analyzer import SpotifyAnalyzer
from src.visualizer import MusicVisualizer
from src.sorters import bubble_sort, quick_sort, merge_sort
from dotenv import load_dotenv
import os

# Initialize Flask app with correct static folder
app = Flask(__name__)

# Load environment variables
load_dotenv()
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Initialize analyzers
analyzer = SpotifyAnalyzer(client_id, client_secret, redirect_uri)
visualizer = MusicVisualizer()


@app.route("/")
def home():
    return send_from_directory("static", "index.html")


@app.route("/static/js/<path:path>")
def serve_js(path):
    return send_from_directory("static/js", path)


@app.route("/api/analyze", methods=["POST"])
def analyze_music():
    data = request.json
    mood = data.get("mood", "happy")
    visualization_type = data.get("visualizationType", "audioFeatures")
    sort_method = data.get("sortMethod", "popularity")

    # Get playlist based on mood
    playlist = analyzer.create_mood_playlist(mood, limit=50)
    tracks_list = playlist.to_dict("records")

    # Apply sorting based on method
    if sort_method == "popularity":
        sorted_tracks = bubble_sort(tracks_list, "popularity", ascending=False)
    elif sort_method == "energy":
        sorted_tracks = quick_sort(tracks_list, "energy", ascending=False)
    elif sort_method == "danceability":
        sorted_tracks = merge_sort(tracks_list, "danceability", ascending=False)

    # Generate visualization based on type
    visualization_data = None
    if visualization_type == "audioFeatures":
        visualization_data = analyzer.get_audio_features_data(playlist)
    elif visualization_type == "genreDistribution":
        visualization_data = analyzer.get_genre_distribution_data(tracks_list)
    elif visualization_type == "topSongs":
        visualization_data = analyzer.get_top_songs_data(tracks_list)

    return jsonify(
        {
            "tracks": sorted_tracks[:10],  # Return top 10 tracks
            "visualizationData": visualization_data,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
