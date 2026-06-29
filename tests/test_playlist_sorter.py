import unittest

from playlistsmith.services.sort_playlist import PlaylistSorter


class PlaylistSorterTests(unittest.TestCase):
    def test_deduplicate_tracks_preserves_first_occurrence(self):
        tracks = [
            {"uri": "spotify:track:1", "name": "First"},
            {"uri": "spotify:track:2", "name": "Second"},
            {"uri": "spotify:track:1", "name": "Duplicated"},
        ]

        deduped = PlaylistSorter._deduplicate_tracks(tracks)

        self.assertEqual([track["uri"] for track in deduped], ["spotify:track:1", "spotify:track:2"])


if __name__ == "__main__":
    unittest.main()
