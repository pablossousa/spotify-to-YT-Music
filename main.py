import spotipy
from spotipy.oauth2 import SpotifyOAuth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import time

# Configurações do Spotify
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
SPOTIFY_REDIRECT_URI = ""
SPOTIFY_SCOPE = "playlist-read-private"

# Configurações do YouTube
YOUTUBE_SCOPES = ["https://www.googleapis.com/auth/youtube"]

# IDs fornecidos pelo usuário
SPOTIFY_PLAYLIST_ID = ""  # Substitua pelo ID da playlist do Spotify
YOUTUBE_PLAYLIST_ID = ""  # Substitua pelo ID da playlist do YouTube

# Posição inicial
START_POSITION = 0  # Substitua pela posição desejada (0-indexado)

# Autenticar no Spotify
def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))
    return sp

# Autenticar no YouTube
def authenticate_youtube():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", YOUTUBE_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    youtube = build("youtube", "v3", credentials=creds)
    return youtube

# Obter músicas de uma playlist do Spotify
def get_spotify_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)
    while results:
        tracks += results["items"]
        results = sp.next(results)
    return [(track["track"]["name"], track["track"]["artists"][0]["name"]) for track in tracks]

# Adicionar música ao YouTube
def add_song_to_youtube(youtube, playlist_id, query):
    search_request = youtube.search().list(
        q=query, part="snippet", maxResults=1, type="video"
    )
    search_response = search_request.execute()
    video_id = search_response["items"][0]["id"]["videoId"]
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id,
                },
            },
        },
    ).execute()

    # Pausar por 8 segundos entre cada requisição
    time.sleep(8)

# Fluxo principal
def main():
    sp = authenticate_spotify()
    youtube = authenticate_youtube()

    # Obter músicas da playlist do Spotify
    print("Obtendo músicas da playlist do Spotify...")
    tracks = get_spotify_playlist_tracks(sp, SPOTIFY_PLAYLIST_ID)

    # Filtrar músicas a partir da posição inicial
    tracks = tracks[START_POSITION:]

    print(f"Adicionando músicas a partir da posição {START_POSITION + 1}...")
    for index, (track, artist) in enumerate(tracks, start=START_POSITION + 1):
        query = f"{track} {artist}"
        print(f"Adicionando {index}: {query}")
        try:
            add_song_to_youtube(youtube, YOUTUBE_PLAYLIST_ID, query)
        except Exception as e:
            print(f"Erro ao adicionar {query}: {e}")

    print("Processo concluído.")

if __name__ == "__main__":
    main()
