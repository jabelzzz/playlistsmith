"""Handles Spotify authentication logic."""

import os
import sys
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Search for the configuration file in different locations
CONFIG_PATH = None
for possible_path in [
    "config.env",  # Current directory
    os.path.join(
        os.path.dirname(__file__), "..", "..", "config.env"
    ),  # From the logic directory
]:
    if os.path.exists(possible_path):
        CONFIG_PATH = possible_path
        break

if not CONFIG_PATH:
    print("Error: No se encontró el archivo de configuración config.env")
    sys.exit(1)

# Load environment variables
load_dotenv(CONFIG_PATH)

# Validate credentials
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):
    print("Error: Faltan credenciales de Spotify en config.env")
    sys.exit(1)


def authenticate_spotify(scope="user-library-read"):
    """Authenticate with Spotify and return a Spotify client.

    Args:
        scope (str, optional): Spotify API scope. Defaults to "user-library-read".

    Returns:
        spotipy.Spotify: Authenticated Spotify client
    """
    try:
        sp_oauth = SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope=scope,
        )

        # Check if a valid token exists
        token_info = sp_oauth.get_cached_token()

        if not token_info:
            # If no cached token, initiate authorization flow
            auth_url = sp_oauth.get_authorize_url()
            print(f"Please visit this URL to authorize the application: {auth_url}")
            response = input("Enter the URL you were redirected to: ")
            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)

        return spotipy.Spotify(auth_manager=sp_oauth)

    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"OAuth authentication error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network request error: {e}")
        return None


def get_saved_tracks(spotify_client, limit=10):
    """Retrieve user's saved tracks.

    Args:
        spotify_client (spotipy.Spotify): Authenticated Spotify client
        limit (int, optional): Number of tracks to retrieve. Defaults to 10.

    Returns:
        list: List of saved tracks
    """
    try:
        results = spotify_client.current_user_saved_tracks(limit=limit)
        return [
            {
                "artist": track["track"]["artists"][0]["name"],
                "name": track["track"]["name"],
            }
            for track in results["items"]
        ]
    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return []
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"OAuth authentication error: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Network request error: {e}")
        return []


if __name__ == "__main__":
    # Load environment variables

    load_dotenv(CONFIG_PATH)

    # Authenticate and get saved tracks
    client = authenticate_spotify()
    if client:
        print(client.current_user()["display_name"])
        saved_tracks = get_saved_tracks(client)
        for idx, track in enumerate(saved_tracks, 1):
            print(f"{idx}. {track['artist']} – {track['name']}")
