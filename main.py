import os
from src.analyzer import SpotifyAnalyzer
from src.visualizer import MusicVisualizer
from src.sorters import bubble_sort, quick_sort, merge_sort
from dotenv import load_dotenv


def main():
    """
    Main function to demonstrate the Spotify analysis and visualization capabilities.

    Features demonstrated:
    1. Mood-based playlist creation
    2. Multiple sorting algorithms
    3. Audio feature visualization
    4. Genre distribution analysis
    5. Artist album analysis
    """
    # load environment variables
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    print(client_id, client_secret, redirect_uri)

    # Initialize analyzers
    analyzer = SpotifyAnalyzer(client_id, client_secret, redirect_uri)
    visualizer = MusicVisualizer()

    # Create mood-based playlist
    print("Creating mood-based playlist...")
    mood_playlist = analyzer.create_mood_playlist("happy", limit=50)

    # Display top 10 happiest songs
    print("\nTop 10 happiest songs:")
    print(mood_playlist[["name", "artist", "valence", "energy"]].head(10))

    # Visualize the audio features and save to file
    visualizer.visualize_audio_features(mood_playlist, save_path="music_analysis.png")
    print("\nVisualization saved as 'music_analysis.png'")

    # Example of sorting by different algorithms
    tracks_list = mood_playlist.to_dict("records")

    print("\nSorting by popularity (Bubble Sort)...")
    sorted_by_popularity = bubble_sort(tracks_list, "popularity", ascending=False)
    print("\nTop 5 most popular tracks:")
    for track in sorted_by_popularity[:5]:
        print(
            f"{track['name']} by {track['artist']} - Popularity: {track['popularity']}"
        )

    print("\nSorting by energy (Quick Sort)...")
    sorted_by_energy = quick_sort(tracks_list, "energy", ascending=False)
    print("\nTop 5 most energetic tracks:")
    for track in sorted_by_energy[:5]:
        print(f"{track['name']} by {track['artist']} - Energy: {track['energy']:.2f}")

    # Create and save the top songs visualization
    visualizer.visualize_top_songs(tracks_list, save_path="top_songs_analysis.png")
    print("\nTop songs visualization saved as 'top_songs_analysis.png'")

    # Analyze artist's albums
    artist_id = analyzer.get_top_artist_id()
    albums_analysis = analyzer.analyze_artist_albums(artist_id)
    print("\nAlbum Analysis (sorted by energy):")
    print(albums_analysis.sort_values("energy", ascending=False))

    # Get and visualize recommendations
    seed_tracks = mood_playlist["id"].head().tolist()
    recommendations = analyzer.recommend_similar_tracks(seed_tracks)
    visualizer.visualize_genre_distribution(
        recommendations.to_dict("records"), save_path="genre_distribution.png"
    )

    # Demonstrate merge sort
    print("\nSorting by danceability (Merge Sort)...")
    sorted_by_danceability = merge_sort(tracks_list, "danceability", ascending=False)
    print("\nTop 5 most danceable tracks:")
    for track in sorted_by_danceability[:5]:
        print(
            f"{track['name']} by {track['artist']} - Danceability: {track['danceability']:.2f}"
        )


if __name__ == "__main__":
    main()
