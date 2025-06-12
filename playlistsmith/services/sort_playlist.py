
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
                self.spotify_client.playlist_replace_items(
                    self.playlist_id, batch)
            else:
                self.spotify_client.playlist_add_items(self.playlist_id, batch)

    def sort_by_artist(self, reverse=False):
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["track"]["uri"], "artist": t["track"]
                ["artists"][0]["name"]}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, key=lambda x: x["artist"], reverse=reverse)
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_release_date(self, reverse=False):
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["track"]["uri"], "release_date": t["track"]
                ["album"]["release_date"]}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, key=lambda x: x["release_date"], reverse=reverse)
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_duration(self, reverse=False):
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["track"]["uri"],
                "duration_ms": t["track"]["duration_ms"]}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, key=lambda x: x["duration_ms"], reverse=reverse)
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_popularity(self, reverse=False):
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["track"]["uri"], "popularity": t["track"]["popularity"]}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, key=lambda x: x["popularity"], reverse=reverse)
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)
