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
    "config.env", # Current directory
    os.path.join(os.path.dirname(__file__), "..", "..", "config.env"), # Parent directory
]:
    if os.path.exists(possible_path):
        CONFIG_PATH = possible_path
        break

if not CONFIG_PATH:
    print("Error: Configuration file config.env not found")
    sys.exit(1)


def validate_spotify_credentials():
    """Validate Spotify credentials from config file."""
    try:
        # Load environment variables from .env file
        load_dotenv(CONFIG_PATH)

        # Validate credentials
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

        if not all([client_id, client_secret, redirect_uri]):
            print("Error: Missing Spotify credentials in config.env")
            sys.exit(1)

        return client_id, client_secret, redirect_uri

    except Exception as e:
        print(f" Error: {e}")
        print("Please follow the setup instructions")
        sys.exit(1)


def authenticate_spotify(scope="user-library-read playlist-modify-public playlist-modify-private"):
    """Authenticate with Spotify and return a Spotify client."""
    try:
        # Get credentials
        client_id, client_secret, redirect_uri = validate_spotify_credentials()

        sp_oauth = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
        )

        # Check if a valid token exists
        token_info = sp_oauth.get_cached_token()

        if not token_info:
            # If no cached token, initiate authorization flow
            auth_url = sp_oauth.get_authorize_url()
            print(
                f"Please visit this URL to authorize the application: {auth_url}"
            )
            response = input("Enter the URL you were redirected to: ")
            code = sp_oauth.parse_response_code(response)
            token_info = sp_oauth.get_access_token(code)
        #TODO: Improve the screen when the user introduce the URL
        return spotipy.Spotify(auth_manager=sp_oauth)

    except spotipy.SpotifyException as e:
        print(f"Spotify API Error: {e}")
        return None
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"OAuth Authentication Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network Request Error: {e}")
        return None


if __name__ == "__main__":
    # Authenticate and get saved tracks
    authenticate_spotify()
