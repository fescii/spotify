# Spotify Music Analyzer

This project analyzes your Spotify listening history using the Spotify API. It creates mood-based playlists and provides visualizations of audio features using various sorting algorithms.

## Prerequisites

- Python 3.8 or higher
- Spotify account
- Git (optional)

## Installation Guide

### 1. Set Up Python Virtual Environment

First, create and activate a Python virtual environment to isolate the project dependencies:

```bash
# Create a new directory for your project (if you haven't already)
mkdir spotify_analyzer
cd spotify_analyzer

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/MacOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 2. Clone or Download the Project

If using Git:
```bash
git clone [repository-url]
cd spotify_analyzer
```

Or download and extract the project files manually.

### 3. Install Dependencies

With the virtual environment activated, install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Set Up Spotify Developer Account

1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the app details:
   - App name: "Music Analyzer" (or any name you prefer)
   - App description: Brief description of your app
   - Redirect URI: `http://localhost:8888/callback`
   - Website: (Optional)
5. Click "Save"
6. On your app's page, note down the following:
   - Client ID
   - Client Secret (click "Show Client Secret" to reveal it)

### 5. Configure Environment Variables

Create a `.env` file in the project root directory:
```bash
touch .env
```

Add your Spotify credentials to the `.env` file:
```plaintext
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=your_redirect_uri_here
```

Replace `your_client_id_here` and `your_client_secret_here` with the values from your Spotify Developer Dashboard, for SPOTIFY_REDIRECT_URI use `http://localhost:8888/callback`.

### 6. Running the Application

With the virtual environment activated, run the main script:
```bash
python main.py or python3 main.py
```
For python 3.x.x in Linux:
```bash
python3 main.py
```

On first run:
1. A browser window will open asking you to log in to Spotify
2. After logging in, authorize the application
3. You'll be redirected to the callback URL
4. The application will start analyzing your music

## Features

- Creates mood-based playlists using audio features
- Visualizes audio features including:
  - Energy vs. Valence
  - Tempo distribution
  - Audio feature distributions
  - Popularity vs. Energy
- Implements multiple sorting algorithms:
  - Bubble Sort
  - Quick Sort
- Saves visualization plots to `music_analysis.png`

## Project Structure
```
spotify_analyzer/
│
├── src/
│   ├── __init__.py
│   ├── analyzer.py           # Main SpotifyAnalyzer class
│   ├── visualizer.py         # Visualization functionality
│   ├── sorters.py           # Sorting algorithms
│   └── utils.py             # Utility functions
│
├── main.py                  # Main script
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables
└── README.md               # Project documentation
```

## Troubleshooting

### Common Issues

1. **Invalid Client Error**
   - Make sure the redirect URI in your Spotify Developer Dashboard exactly matches `http://localhost:8888/callback`
   - Check that your Client ID and Client Secret are correctly copied to the `.env` file

2. **Authentication Failed**
   - Ensure you're logged into the correct Spotify account
   - Try clearing your browser cookies and cache

3. **ModuleNotFoundError**
   - Make sure your virtual environment is activated
   - Verify all dependencies are installed: `pip install -r requirements.txt`

4. **Visualization Issues**
   - If plots don't display, check that `music_analysis.png` was created in your project directory
   - Ensure you have sufficient disk space for saving plots

### Still Having Issues?

- Check that all files are in the correct directory structure
- Verify your Python version: `python --version`
- Make sure all environment variables are set correctly
- Try deactivating and reactivating the virtual environment

## Contributing

Feel free to fork the repository and submit pull requests with improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.