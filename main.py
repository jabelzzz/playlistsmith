import sys
from playlistsmith.logic.spotify_auth import authenticate_spotify
from playlistsmith.logic.sort_playlist import PlaylistManager


def main():
    """Main function to authenticate and manage playlists."""
    user = authenticate_spotify()
    if not user:
        sys.exit(1)
    print("Bienvenido a PlaylistSmith", user.current_user()["display_name"])
    print("Sus Playlist disponibles son:")
    playlists = user.current_user_playlists()
    for playlist in playlists["items"]:
        print(playlist["name"],"-",playlist["id"])
    
    


if __name__ == "__main__":
    main()
