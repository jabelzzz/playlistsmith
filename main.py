import sys
from playlistsmith.logic.spotify_auth import authenticate_spotify
from playlistsmith.logic.sort_playlist import PlaylistSorter


def main():
    """Main function to authenticate and manage playlists."""
    spotify_client = authenticate_spotify(
        scope="user-library-read playlist-modify-public playlist-modify-private"
    )
    if not spotify_client:
        sys.exit(1)

    print(f"Welcome to PlaylistSmith {spotify_client.current_user()['display_name']}")

    # Get playlists
    print("\nYour available playlists:")
    playlists = spotify_client.current_user_playlists()

    for i, playlist in enumerate(playlists["items"], 1):
        print(f"{i}. {playlist['name']} - {playlist['id']}")

    # Select playlist to sort
    try:
        selection = (
            int(input("\nEnter the number of the playlist you want to sort: ")) - 1
        )
        selected_playlist = playlists["items"][selection]
        print(f"\nYou selected: {selected_playlist['name']}")
        option = input(
            """How would you like to sort it?
            1. Artist
            2. Release date
            3. Duration
            4. Popularity
            Enter the option: """
        )
        sorter = PlaylistSorter(spotify_client)
        if option == "1":
            sorter.sort_by_artist(selected_playlist["id"])
        elif option == "2":
            sorter.sort_by_release_date(selected_playlist["id"])
        elif option == "3":
            sorter.sort_by_duration(selected_playlist["id"])
        elif option == "4":
            sorter.sort_by_popularity(selected_playlist["id"])

    except (ValueError, IndexError):
        print("Invalid selection. Please try again.")
        return


if __name__ == "__main__":
    main()
