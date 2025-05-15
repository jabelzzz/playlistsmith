"""Clase para gestionar y ordenar playlists de Spotify."""

import spotipy
from typing import List, Dict, Optional
from spotipy.oauth2 import SpotifyOAuth


class PlaylistManager:
    """Gestiona operaciones con playlists de Spotify."""

    def __init__(self, spotify_client: spotipy.Spotify):
        """Inicializa el gestor con un cliente de Spotify."""
        self.spotify = spotify_client


    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """Gets all tracks from a playlist with their details."""
        results = self.spotify.playlist_tracks(playlist_id)
        tracks = results["items"]
        # Manage pagination if there are more than 100 tracks
        while results["next"]:
            results = self.spotify.next(results)
            tracks.extend(results["items"])
        return [
            {
                "id": track["track"]["id"],
                "name": track["track"]["name"],
                "artists": [artist["name"] for artist in track["track"]["artists"]],
                "album": track["track"]["album"]["name"],
                "duration_ms": track["track"]["duration_ms"],
                "popularity": track["track"]["popularity"],
                "release_date": track["track"]["album"]["release_date"],
            }
            for track in tracks
        ]


    def get_playlist_info(self, playlist_id: str) -> Dict:
        """Gets basic information about a playlist."""
        playlist_info = self.spotify.playlist(playlist_id)
        print(playlist_info.keys())
        return {
            "name": playlist_info["name"],
            "description": playlist_info["description"],
            "public": playlist_info["public"],
            "collaborative": playlist_info["collaborative"],
            "owner": playlist_info["owner"]["display_name"],
        }


class PlaylistSorter:
    """Clase que implementa diferentes métodos de ordenamiento."""

    def __init__(self, playlist_manager: PlaylistManager):
        """Inicializa el ordenador con un gestor de playlist."""
        self.playlist_manager = playlist_manager

    def sort_by_popularity(self, playlist_id: str) -> List[Dict]:
        """Sorts tracks by popularity."""
        # Implementar
        pass

    def sort_by_release_date(self, playlist_id: str) -> List[Dict]:
        """Sorts tracks by release date."""
        # Implementar
        pass

    def sort_by_duration(self, playlist_id: str) -> List[Dict]:
        """Sorts tracks by duration."""
        # Implementar
        pass

    def sort_by_artist(self, playlist_id: str) -> List[Dict]:
        """Sorts tracks by artist."""
        # Implementar
        pass


def create_playlist_sorter(spotify_client: spotipy.Spotify) -> PlaylistSorter:
    """Creates and returns a PlaylistSorter object initialized."""
    manager = PlaylistManager(spotify_client)
    return PlaylistSorter(manager)
