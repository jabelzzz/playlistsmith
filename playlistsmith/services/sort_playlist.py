import spotipy
from playlistsmith.services.spotify_auth import authenticate_spotify


class PlaylistSorter:
    """Class that implements different sorting methods."""

    def __init__(self, spotify_client: spotipy.Spotify):
        """Initialize the sorter module with an already authenticated Spotify client."""
        self.spotify_client = spotify_client
        if not self.spotify_client:
            raise ValueError(
                "Spotify client is not authenticated. Please authenticate first."
            )

    def get_all_tracks(self, playlist_id: str):
        """
        Retrieve all tracks from a playlist, handling pagination.

        Args:
            playlist_id (str): ID of the Spotify playlist

        Returns:
            list: A list of all tracks in the playlist
        """
        tracks = []
        offset = 0
        limit = 100
        # TODO: Check the logic here to use the spotify_client here to obtain the results
        while True:
            results = self.spotify_client.playlist["items"]
            tracks.extend(results["items"])

            # Check if there are more tracks to fetch
            if len(results["items"]) < limit:
                break

            offset += limit

        return tracks

    def reorder_playlist_in_batches(self, playlist_id: str, track_uris: list):
        """
        Reorder a playlist in batches of 100 tracks.

        Args:
            playlist_id (str): ID of the Spotify playlist
            track_uris (list): List of track URIs to reorder
        """
        for index in range(0, len(track_uris), 100):
            batch = track_uris[index: index + 100]
            if index == 0:
                # Replace the initial items in the playlist
                self.spotify_client.playlist_replace_items(playlist_id, batch)
            else:
                # Add the remaining items to the playlist
                self.spotify_client.playlist_add_items(playlist_id, batch)

    def sort_by_artist(self, playlist_id: str):
        """
        Sort a playlist by artist name.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get all playlist tracks
        tracks = self.get_all_tracks(playlist_id)

        if not tracks:
            print("No tracks found in the playlist.")
            return

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

        # Reorder the playlist
        while True:
            order = input("Choose the order:\n1. A to Z\n2. Z to A\n> ")
            if order == "1":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["artist"], reverse=False
                )
                break
            elif order == "2":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["artist"], reverse=True
                )
                break
            else:
                print("Invalid option. Please choose 1 or 2.")

        track_uris = [track["uri"] for track in sorted_tracks]
        self.reorder_playlist_in_batches(playlist_id, track_uris)

    def sort_by_release_date(self, playlist_id: str):
        """
        Sort a playlist by release date.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        tracks = self.get_all_tracks(playlist_id)
        if not tracks:
            print("No tracks found in the playlist.")
            return
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

        # Reorder the playlist
        while True:
            order = input(
                "Choose the order:\n1. Newest to Oldest\n2. Oldest to Newest\n> "
            )
            if order == "1":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["release_date"], reverse=True
                )
                break
            elif order == "2":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["release_date"], reverse=False
                )
                break
        track_uris = [track["uri"] for track in sorted_tracks]
        # Reemplazar la lista de reproducción en lotes
        self.reorder_playlist_in_batches(playlist_id, track_uris)

    def sort_by_duration(self, playlist_id: str):
        """
        Sort a playlist by track duration.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        tracks = self.get_all_tracks(playlist_id)
        if not tracks:
            print("No tracks found in the playlist.")
            return
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

        # Reorder the playlist
        while True:
            order = input(
                "Choose the order:\n1. Longest to Shortest\n2. Shortest to Longest\n> "
            )
            if order == "1":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["duration_ms"], reverse=True
                )
                break
            elif order == "2":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["duration_ms"], reverse=False
                )
                break

        track_uris = [track["uri"] for track in sorted_tracks]
        # Reemplazar la lista de reproducción en lotes
        self.reorder_playlist_in_batches(playlist_id, track_uris)

    def sort_by_popularity(self, playlist_id: str):
        """
        Sort a playlist by popularity.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        tracks = self.get_all_tracks(playlist_id)
        if not tracks:
            print("No tracks found in the playlist.")
            return
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
        # Reorder the playlist
        while True:
            order = input(
                "Choose the order:"
                "\n1. Most popular to Least popular"
                "\n2. Least popular to Most popular\n> "
            )
            if order == "1":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["popularity"], reverse=True
                )
                break
            elif order == "2":
                print("Sorting songs...")
                sorted_tracks = sorted(
                    track_data, key=lambda x: x["popularity"], reverse=False
                )
                break

        track_uris = [track["uri"] for track in sorted_tracks]
        # Reemplazar la lista de reproducción en lotes
        self.reorder_playlist_in_batches(playlist_id, track_uris)
