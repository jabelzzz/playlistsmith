"""Clase para gestionar y ordenar playlists de Spotify."""

import spotipy
from playlistsmith.logic.spotify_auth import authenticate_spotify


class PlaylistSorter:
    """Clase que implementa diferentes métodos de ordenamiento."""

    def __init__(self, spotify_client: spotipy.Spotify):
        """Inicializa el modulo ordenador con un cliente de spotify ya logueado"""
        self.spotify_client = spotify_client

    def sort_by_popularity(self, playlist_id: str):
        """Ordena una playlist por popularidad."""
        tracks = self.spotify_client.playlist_tracks(playlist_id)["items"]
        return tracks

    def sort_by_song_release_date(self, playlist_id: str):
        """
        Ordena una playlist por fecha de lanzamiento de las canciones.

        Args:
            playlist_id (str): ID de la playlist de Spotify a ordenar
        """
        # Obtener los tracks de la playlist
        results = self.spotify_client.playlist_tracks(playlist_id)
        tracks = results["items"]

        # Extraer la información relevante de cada track
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

        # Ordenar por fecha de lanzamiento (más antiguo a más reciente)
        sorted_tracks = sorted(
            track_data, key=lambda x: x["release_date"], reverse=True)

        # Reordenar la playlist
        track_uris = [track["uri"] for track in sorted_tracks]
        self.spotify_client.playlist_replace_items(playlist_id, track_uris)
