from playlistsmith.services.spotify_auth import authenticate_spotify
from playlistsmith.ui.main_window import MainWindow


def main():
    # Autentica al usuario antes de lanzar la interfaz
    spotify_client = authenticate_spotify()
    if not spotify_client:
        print("No se pudo autenticar con Spotify.")
        return
    app = MainWindow(spotify_client)
    app.mainloop()


if __name__ == "__main__":
    main()
