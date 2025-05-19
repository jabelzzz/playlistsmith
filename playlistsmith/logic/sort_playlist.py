"""Class to manage and sort Spotify playlists."""

import spotipy
from playlistsmith.logic.spotify_auth import authenticate_spotify


class PlaylistSorter:
    """Class that implements different sorting methods."""

    def __init__(self, spotify_client: spotipy.Spotify):
        """Initialize the sorter module with an already authenticated Spotify client."""
        self.spotify_client = spotify_client
#TODO: Obtener todas las canciones, actualmente solo obtienen 100
    def sort_by_artist(self, playlist_id: str):
        """
        Sort a playlist by artist name.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        results = self.spotify_client.playlist_tracks(playlist_id)
        tracks = results["items"]

        # Extract relevant information from each track
        track_data = []
        for item in tracks:
            track = item["track"]
            track_data.append(
                {
                    "uri": track["uri"],
                    "artist": track["artists"][0]["name"],
                    "name": track["name"],
                }
            )

        # Sort by artist name (A-Z)
        sorted_tracks = sorted(track_data, key=lambda x: x["artist"])

        # Reorder the playlist
        track_uris = [track["uri"] for track in sorted_tracks]
        self.spotify_client.playlist_replace_items(playlist_id, track_uris)

    def sort_by_release_date(self, playlist_id: str):
        """
        Sort a playlist by release date.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        results = self.spotify_client.playlist_tracks(playlist_id)
        tracks = results["items"]

        # Extract relevant information from each track
        track_data = []
        for item in tracks:
            track = item["track"]
            track_data.append(
                {
                    "uri": track["uri"],
                    "release_date": track["album"]["release_date"],
                    "name": track["name"],
                }
            )

        # Sort by release date (oldest to newest)
        sorted_tracks = sorted(
            track_data, key=lambda x: x["release_date"], reverse=True
        )

        # Reorder the playlist
        track_uris = [track["uri"] for track in sorted_tracks]
        self.spotify_client.playlist_replace_items(playlist_id, track_uris)

    def sort_by_duration(self, playlist_id: str):

        """
        Sort a playlist by track duration.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        results = self.spotify_client.playlist_tracks(playlist_id)
        tracks = results["items"]

        # Extract relevant information from each track
        track_data = []
        for item in tracks:
            track = item["track"]
            track_data.append(
                {
                    "uri": track["uri"],
                    "duration_ms": track["duration_ms"],
                    "name": track["name"],
                }
            )

        # Sort by duration (shortest to longest)
        sorted_tracks = sorted(track_data, key=lambda x: x["duration_ms"])

        # Reorder the playlist
        track_uris = [track["uri"] for track in sorted_tracks]
        self.spotify_client.playlist_replace_items(playlist_id, track_uris)

    def sort_by_popularity(self, playlist_id: str):
        """
        Sort a playlist by popularity.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        results = self.spotify_client.playlist_tracks(playlist_id)
        tracks = results["items"]

        # Extract relevant information from each track
        track_data = []
        for item in tracks:
            track = item["track"]
            track_data.append(
                {
                    "uri": track["uri"],
                    "popularity": track["popularity"],
                    "name": track["name"],
                }
            )

        # Sort by release date (oldest to newest)
        sorted_tracks = sorted(track_data, key=lambda x: x["popularity"], reverse=True)

        # Reorder the playlist
        track_uris = [track["uri"] for track in sorted_tracks]
        self.spotify_client.playlist_replace_items(playlist_id, track_uris)
