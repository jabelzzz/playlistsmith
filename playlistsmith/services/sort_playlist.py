
class PlaylistSorter:
    """Class that implements different sorting methods."""

    def __init__(self, spotify_client, playlist_id: str):
        """Initialize the sorter module with an already authenticated Spotify client."""
        self.spotify_client = spotify_client
        self.playlist_id = playlist_id
        if not self.spotify_client:
            raise ValueError(
                "Spotify client is not authenticated. Please authenticate first."
            )

    def get_all_tracks(self):
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
        while True:
            results = self.spotify_client.playlist["items"]
            tracks.extend(results["items"])

            if len(results["items"]) < limit:
                break

            offset += limit

        return tracks

    def reorder_playlist_in_batches(self, track_uris: list):
        """
        Reorder a playlist in batches of 100 tracks.

        Args:
            track_uris (list): List of track URIs to reorder
        """
        for index in range(0, len(track_uris), 100):
            batch = track_uris[index: index + 100]
            if index == 0:
                self.spotify_client.playlist_replace_items(self.playlist_id, batch)
            else:
                self.spotify_client.playlist_add_items(self.playlist_id, batch)

    def sort_by_artist(self):
        """
        Sort a playlist by artist name.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        tracks = self.get_all_tracks()

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
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_release_date(self):
        """
        Sort a playlist by release date.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        tracks = self.get_all_tracks()
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
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_duration(self):
        """
        Sort a playlist by track duration.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        tracks = self.get_all_tracks()
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
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_popularity(self):
        """
        Sort a playlist by popularity.

        Args:
            playlist_id (str): ID of the Spotify playlist to sort
        """
        # Get playlist tracks
        tracks = self.get_all_tracks()
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
        self.reorder_playlist_in_batches(track_uris)
