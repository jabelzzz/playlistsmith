from playlistsmith.services.spotify_auth import authenticate_spotify
from playlistsmith.ui.main_window import MainWindow


def main():
    # Authenticate the user before launching the interface
    spotify_client = authenticate_spotify()
    if not spotify_client:
        print("Could not authenticate with Spotify.")
        return
    app = MainWindow(spotify_client)
    app.mainloop()


if __name__ == "__main__":
    main()
