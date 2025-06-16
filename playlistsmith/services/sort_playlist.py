class PlaylistSorter:
    """A class that provides various sorting methods for Spotify playlists.
    
    This class handles sorting of tracks in a Spotify playlist based on different criteria
    such as artist name, release date, duration, and popularity.
    """

    def __init__(self, spotify_client, playlist_id: str):
        """Initialize the PlaylistSorter with Spotify client and playlist ID.
        
        Args:
            spotify_client: An authenticated Spotify client instance.
            playlist_id (str): The ID of the playlist to be sorted.
            
        Raises:
            ValueError: If the Spotify client is not authenticated.
        """
        self.spotify_client = spotify_client
        self.playlist_id = playlist_id
        if not self.spotify_client:
            raise ValueError(
                "Spotify client is not authenticated. Please authenticate first."
            )

    def get_all_tracks(self):
        """Retrieve all tracks from the playlist, handling pagination.
        
        Returns:
            list: A list of all track items in the playlist with their details.
        """
        all_tracks = []
        limit = 100
        offset = 0
        
        while True:
            response = self.spotify_client.playlist_items(
                self.playlist_id,
                limit=limit,
                offset=offset,
                fields='items(track(id,uri,name,artists,album(name,release_date),duration_ms,popularity)),next'
            )
            
            if not response or 'items' not in response:
                break
                
            # Filtrar pistas nulas y extraer solo la información necesaria
            tracks = []
            for item in response['items']:
                if item and item.get('track'):
                    track = item['track']
                    tracks.append({
                        'id': track.get('id'),
                        'uri': track.get('uri'),
                        'name': track.get('name'),
                        'artists': track.get('artists', []),
                        'album': track.get('album', {}),
                        'duration_ms': track.get('duration_ms', 0),
                        'popularity': track.get('popularity', 0)
                    })
            
            all_tracks.extend(tracks)
            
            # Si no hay más páginas, salir del bucle
            if not response.get('next'):
                break
                
            offset += limit
            
        return all_tracks

    def reorder_playlist_in_batches(self, track_uris: list):
        """Reorder a playlist in batches of 100 tracks.
        
        Args:
            track_uris (list): List of track URIs in the desired order.
            
        Note:
            Spotify's API has a limit of 100 tracks per request, so this method
            handles larger playlists by making multiple requests as needed.
        """
        for index in range(0, len(track_uris), 100):
            batch = track_uris[index: index + 100]
            if index == 0:
                self.spotify_client.playlist_replace_items(
                    self.playlist_id, batch)
            else:
                self.spotify_client.playlist_add_items(self.playlist_id, batch)

    def sort_by_artist(self, reverse=False):
        """Sort the playlist by artist name.
        
        Args:
            reverse (bool, optional): If True, sorts in reverse order (Z-A).
                                    Defaults to False (A-Z).
        """
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["uri"], "artist": t["artists"][0]["name"]}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, key=lambda x: x["artist"].lower(), reverse=reverse)
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_release_date(self, reverse=True):
        """Sort the playlist by track release date.
        
        Args:
            reverse (bool, optional): If True, sorts from newest to oldest.
                                    Defaults to True.
        """
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        def get_release_date(track):
            # Handle different date formats (YYYY, YYYY-MM, YYYY-MM-DD)
            date_str = track.get("album", {}).get("release_date", "")
            parts = date_str.split('-')
            year = int(parts[0]) if parts[0].isdigit() else 0
            month = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
            day = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 1
            return (year, month, day)

        track_data = [
            {"uri": t["uri"], "release_date": get_release_date(t)}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, 
            key=lambda x: x["release_date"], 
            reverse=reverse
        )
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_duration(self, reverse=True):
        """Sort the playlist by track duration.
        
        Args:
            reverse (bool, optional): If True, sorts from longest to shortest.
                                    Defaults to True.
        """
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["uri"], "duration": t.get("duration_ms", 0)}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, 
            key=lambda x: x["duration"], 
            reverse=reverse
        )
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)

    def sort_by_popularity(self, reverse=True):
        """Sort the playlist by track popularity.
        
        Args:
            reverse (bool, optional): If True, sorts from most to least popular.
                                    Defaults to True (most popular first).
        """
        tracks = self.get_all_tracks()
        if not tracks:
            print("No tracks found.")
            return

        track_data = [
            {"uri": t["uri"], "popularity": t.get("popularity", 0)}
            for t in tracks
        ]

        sorted_tracks = sorted(
            track_data, 
            key=lambda x: x["popularity"], 
            reverse=reverse
        )
        track_uris = [t["uri"] for t in sorted_tracks]
        self.reorder_playlist_in_batches(track_uris)
