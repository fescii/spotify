Here's a `SERVER.md` file that provides comprehensive instructions for setting up, installing, and running the server for your Spotify music analysis project.

---

# SERVER.md

## Project Overview
This project is a Spotify music analysis web application that uses the Spotify API to analyze music features, create mood-based playlists, and provide visualizations such as audio features, genre distributions, and top songs.

## Prerequisites
Before starting, ensure you have the following:
- Python 3.7+
- A Spotify Developer Account with a registered application to obtain `client_id` and `client_secret`
- Flask and Spotipy installed for the server

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Environment Variables
Create a `.env` file in the project root directory to store sensitive information such as Spotify API credentials.

Example `.env`:
```dotenv
SPOTIFY_CLIENT_ID=<your_spotify_client_id>
SPOTIFY_CLIENT_SECRET=<your_spotify_client_secret>
SPOTIFY_REDIRECT_URI=<your_redirect_uri>
```

- Replace `<your_spotify_client_id>` and `<your_spotify_client_secret>` with your Spotify API credentials.
- Set `<your_redirect_uri>` to match the redirect URI specified in your Spotify Developer Dashboard (e.g., `http://127.0.0.1:5000/callback`).

### 3. Install Python Dependencies
Use the following command to install the required Python packages:
```bash
pip install -r requirements.txt
```

The `requirements.txt` should contain:
```plaintext
Flask
spotipy
pandas
python-dotenv
```

### 4. File Structure Overview
Your project directory should look like this:
```
project-root/
│
├── src/
│   ├── analyzer.py          # Contains the SpotifyAnalyzer class
│   ├── visualizer.py        # Contains visualization classes
│   ├── sorters.py           # Sorting algorithms
│
├── static/
│   ├── js/
│   │   └── main.js          # Main JavaScript file handling front-end functionality
│   ├── index.html           # HTML file for front-end layout
│
├── .env                     # Environment variables for sensitive data
├── requirements.txt         # Python dependencies
|── SERVER.md                # Project server setup instructions
|── README.md                # Project terminal setup instructions
└── server.py                # Main server file
```

## Running the Server

### 1. Start the Flask Server
In the project root directory, start the Flask server:
```bash
python server.py
```

The server will start by default on `http://127.0.0.1:5000`.

### 2. Open the Application
After starting the server, open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. API Endpoints
- **`/api/analyze`**: This POST endpoint analyzes music based on the provided mood, visualization type, and sorting method. 
  - Request Body:
    ```json
    {
      "mood": "happy",
      "visualizationType": "audioFeatures",
      "sortMethod": "popularity"
    }
    ```
  - Response: Returns sorted tracks and `visualizationData` for the specified chart type.

## Notes

- **Spotify API Rate Limits**: Be mindful of API rate limits. Avoid requesting data for a large number of items in a short time span.
- **Authentication**: The application uses Spotify's OAuth 2.0 for authentication. Ensure that your redirect URI in `.env` matches the one in your Spotify Developer Dashboard.
  
### Troubleshooting

- **Error: `TypeError: n is undefined`**  
  Check that the data returned from the API endpoint matches the expected format for the frontend visualization.

- **Invalid Client ID/Secret**  
  Double-check your `.env` file to ensure the correct Spotify credentials are provided.

---