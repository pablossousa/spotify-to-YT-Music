# Spotify to YouTube Playlist Sync

A Python script that copies songs from a Spotify playlist to a YouTube playlist by searching each track on YouTube and automatically adding the first matching video.

This project uses the **Spotify Web API** and the **YouTube Data API v3** for authentication and playlist management.

---

## Features

* Read all tracks from a Spotify playlist
* Search each song on YouTube
* Add videos to an existing YouTube playlist
* Resume synchronization from any position in the Spotify playlist
* OAuth authentication for both Spotify and YouTube
* Configurable delay between API requests to reduce rate limiting

---

## Technologies

* Python 3
* Spotipy
* Spotify Web API
* YouTube Data API v3
* Google OAuth 2.0

---

## Requirements

Install the required dependencies:

```bash
pip install spotipy google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

---

## Setup

### 1. Spotify API

Create an application in the Spotify Developer Dashboard.

Fill in the following variables:

```python
SPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
SPOTIFY_REDIRECT_URI = "YOUR_REDIRECT_URI"
```

The required scope is:

```text
playlist-read-private
```

---

### 2. YouTube API

1. Create a project in Google Cloud Console.
2. Enable the **YouTube Data API v3**.
3. Create OAuth 2.0 credentials.
4. Download the credentials file.
5. Rename it to:

```
credentials.json
```

Place the file in the project's root directory.

The first execution will open a browser window for authentication and automatically generate:

```
token.pickle
```

This file stores your access token for future executions.

---

## Configuration

Before running the script, configure:

```python
SPOTIFY_PLAYLIST_ID = "YOUR_SPOTIFY_PLAYLIST_ID"

YOUTUBE_PLAYLIST_ID = "YOUR_YOUTUBE_PLAYLIST_ID"

START_POSITION = 0
```

| Variable              | Description                                             |
| --------------------- | ------------------------------------------------------- |
| `SPOTIFY_PLAYLIST_ID` | Spotify playlist ID                                     |
| `YOUTUBE_PLAYLIST_ID` | Destination YouTube playlist ID                         |
| `START_POSITION`      | Index from which synchronization should start (0-based) |

---

## Usage

Run the script:

```bash
python main.py
```

Example output:

```text
Getting tracks from Spotify playlist...

Adding songs starting from position 51...

Adding 51: Viva La Vida Coldplay

Adding 52: Yellow Coldplay

Adding 53: Paradise Coldplay

Process completed.
```

---

## How It Works

1. Authenticate with Spotify.
2. Authenticate with YouTube.
3. Retrieve all tracks from the Spotify playlist.
4. Build a search query using:

```
Track Name + Artist Name
```

5. Search YouTube for the first matching video.
6. Add the video to the specified YouTube playlist.
7. Wait 8 seconds before processing the next track.

---

## Project Structure

```
.
├── main.py
├── credentials.json
├── token.pickle
└── README.md
```

---

## Notes

* The script always adds the **first YouTube search result**.
* Song matches may not always be the official version.
* Existing songs in the YouTube playlist are **not checked**, so duplicates may occur.
* A delay is included between requests to reduce the chance of hitting YouTube API rate limits.

---

## Future Improvements

* Detect duplicate videos before adding them.
* Better search ranking using song duration and metadata.
* Support multiple artists.
* Command-line arguments for playlist IDs.
* Progress bar and synchronization statistics.
* Export synchronization logs.

---

## License

This project is available under the MIT License.

---

## Author

**Pablo Sousa**

Computer Engineering student at CEFET-MG

GitHub: https://github.com/pablossousa
