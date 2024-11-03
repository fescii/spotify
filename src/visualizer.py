import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict


class MusicVisualizer:
    """
    A class for creating visualizations of music data and audio features.

    Features:
    - Audio feature visualization
    - Top songs analysis
    - Album energy comparison
    - Genre distribution charts
    """

    def __init__(self):
        # Set style for all plots
        plt.style.use("seaborn-v0_8")
        sns.set_palette("husl")

    def setup_plot(self):
        """Setup the plot with proper styling"""
        fig = plt.figure(figsize=(15, 10))
        fig.patch.set_facecolor("white")
        return fig

    def visualize_genre_distribution(
        self, tracks: List[Dict], save_path: str = None
    ) -> None:
        genres = []
        for track in tracks:
            # Check if the "artists" key exists and has at least one entry
            if "artists" in track and track["artists"]:
                artist_id = track["artists"][0]["id"]
                artist_info = self.sp.artist(artist_id)
                genres.extend(
                    artist_info.get("genres", [])
                )  # Get genres or an empty list if not available

        if not genres:
            print("No genres found to visualize.")
            return

        genre_counts = pd.Series(genres).value_counts().head(10)

        plt.figure(figsize=(12, 8))
        plt.pie(genre_counts.values, labels=genre_counts.index, autopct="%1.1f%%")
        plt.title("Top 10 Genres Distribution")

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            plt.close()
        else:
            plt.show()

    def visualize_audio_features(self, df: pd.DataFrame, save_path: str = None) -> None:
        """Create visualizations for audio features with improved styling"""
        fig = self.setup_plot()

        # Create scatter plot of energy vs. valence
        ax1 = plt.subplot(2, 2, 1)
        sns.scatterplot(data=df, x="energy", y="valence", alpha=0.6, ax=ax1)
        ax1.set_xlabel("Energy", fontsize=10)
        ax1.set_ylabel("Valence", fontsize=10)
        ax1.set_title("Energy vs. Valence", fontsize=12, pad=15)
        ax1.grid(True, linestyle="--", alpha=0.7)

        # Create histogram of tempos
        ax2 = plt.subplot(2, 2, 2)
        sns.histplot(data=df, x="tempo", bins=30, ax=ax2)
        ax2.set_xlabel("Tempo (BPM)", fontsize=10)
        ax2.set_ylabel("Count", fontsize=10)
        ax2.set_title("Distribution of Tempo", fontsize=12, pad=15)
        ax2.grid(True, linestyle="--", alpha=0.7)

        # Create box plot of main features
        ax3 = plt.subplot(2, 2, 3)
        features_to_plot = ["danceability", "energy", "valence"]
        df_melted = df[features_to_plot].melt()
        sns.boxplot(data=df_melted, x="variable", y="value", ax=ax3)
        ax3.set_xlabel("Feature", fontsize=10)
        ax3.set_ylabel("Value", fontsize=10)
        ax3.set_title("Distribution of Audio Features", fontsize=12, pad=15)
        ax3.grid(True, linestyle="--", alpha=0.7)

        # Create popularity vs. energy scatter plot
        ax4 = plt.subplot(2, 2, 4)
        sns.scatterplot(data=df, x="popularity", y="energy", alpha=0.6, ax=ax4)
        ax4.set_xlabel("Popularity", fontsize=10)
        ax4.set_ylabel("Energy", fontsize=10)
        ax4.set_title("Popularity vs. Energy", fontsize=12, pad=15)
        ax4.grid(True, linestyle="--", alpha=0.7)

        # Adjust layout and add title
        plt.suptitle("Music Analysis Dashboard", fontsize=14, y=1.02)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            plt.close()
        else:
            plt.show()

    def visualize_top_songs(self, tracks_list: list, save_path: str = None) -> None:
        """Create visualizations for top 10 songs with different sorting methods"""
        # Create a figure with 3 subplots
        fig = plt.figure(figsize=(15, 12))
        fig.patch.set_facecolor("white")

        # Helper function to create horizontal bar charts
        def create_horizontal_bars(ax, data, x_key, title):
            names = [f"{track['name']} - {track['artist']}" for track in data[:10]]
            values = [track[x_key] for track in data[:10]]

            # Create horizontal bars
            bars = ax.barh(range(len(names)), values, alpha=0.8)

            # Customize the plot
            ax.set_yticks(range(len(names)))
            ax.set_yticklabels(names, fontsize=8)
            ax.set_title(title, pad=20, fontsize=12)
            ax.grid(True, linestyle="--", alpha=0.7)

            # Add value labels on bars
            for i, bar in enumerate(bars):
                width = bar.get_width()
                # Add a small offset to the x position to prevent overlap
                ax.text(
                    width + (max(values) * 0.02),
                    bar.get_y() + bar.get_height() / 2,
                    (
                        f"{values[i]:.2f}"
                        if isinstance(values[i], float)
                        else str(values[i])
                    ),
                    ha="left",
                    va="center",
                    fontsize=8,
                )

        # Plot 1: Top 10 by Mood Score (if available) or Valence
        ax1 = plt.subplot(3, 1, 1)
        if "mood_score" in tracks_list[0]:
            mood_sorted = sorted(tracks_list, key=lambda x: x["mood_score"])
            create_horizontal_bars(
                ax1,
                mood_sorted,
                "mood_score",
                "Top 10 Songs by Mood Score (Lower is Better)",
            )
        else:
            valence_sorted = sorted(
                tracks_list, key=lambda x: x["valence"], reverse=True
            )
            create_horizontal_bars(
                ax1, valence_sorted, "valence", "Top 10 Songs by Valence"
            )

        # Plot 2: Top 10 by Popularity
        ax2 = plt.subplot(3, 1, 2)
        popularity_sorted = sorted(
            tracks_list, key=lambda x: x["popularity"], reverse=True
        )
        create_horizontal_bars(
            ax2, popularity_sorted, "popularity", "Top 10 Songs by Popularity"
        )

        # Plot 3: Top 10 by Energy
        ax3 = plt.subplot(3, 1, 3)
        energy_sorted = sorted(tracks_list, key=lambda x: x["energy"], reverse=True)
        create_horizontal_bars(ax3, energy_sorted, "energy", "Top 10 Songs by Energy")

        # Adjust layout
        plt.suptitle("Top Songs Analysis", fontsize=14, y=0.95)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            plt.close()
        else:
            plt.show()
