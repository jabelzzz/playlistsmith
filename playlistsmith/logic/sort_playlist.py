"""Class to manage and sort Spotify playlists."""

import spotipy
from playlistsmith.logic.spotify_auth import authenticate_spotify


class PlaylistSorter:
    """Class that implements different sorting methods."""

    def __init__(self, spotify_client: spotipy.Spotify):
        """Initialize the sorter module with an already authenticated Spotify client."""
        self.spotify_client = spotify_client

    def sort_by_popularity(self, playlist_id: str):
        """Sort a playlist by popularity."""
        tracks = self.spotify_client.playlist_tracks(playlist_id)["items"]
        return tracks

    def sort_by_song_release_date(self, playlist_id: str):
        """
        Sort a playlist by song release date.

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
            track_data, key=lambda x: x["release_date"], reverse=True)

        # Reorder the playlist
        track_uris = [track["uri"] for track in sorted_tracks]
        self.spotify_client.playlist_replace_items(playlist_id, track_uris)
