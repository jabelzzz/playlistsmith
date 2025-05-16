import sys
from playlistsmith.logic.spotify_auth import authenticate_spotify
from playlistsmith.logic.sort_playlist import PlaylistSorter


def main():
    """Función principal para autenticar y gestionar listas de reproducción."""
    spotify_client = authenticate_spotify(scope="user-library-read playlist-modify-public playlist-modify-private")
    if not spotify_client:
        sys.exit(1)

    print(f"Bienvenido a PlaylistSmith {spotify_client.current_user()['display_name']}")

    # Obtener listas de reproducción
    print("\nTus listas de reproducción disponibles son:")
    playlists = spotify_client.current_user_playlists()

    for i, playlist in enumerate(playlists["items"], 1):
        print(f"{i}. {playlist['name']} - {playlist['id']}")

    # Seleccionar lista para ordenar
    try:
        selection = (
            int(input("\nSelecciona el número de la lista que deseas ordenar: ")) - 1
        )
        selected_playlist = playlists["items"][selection]
        print(f"\nHas seleccionado: {selected_playlist['name']}")
        option = input("""¿Como deseas ordenarla?
        1. Por popularidad
        2. Por fecha de lanzamiento de las canciones
        """)
        sorter = PlaylistSorter(spotify_client)
        if option == "1":
            sorter.sort_by_popularity(selected_playlist["id"])
        elif option == "2":
            sorter.sort_by_song_release_date(selected_playlist["id"])

    except (ValueError, IndexError):
        print("Selección inválida. Por favor, intenta de nuevo.")
        return


if __name__ == "__main__":
    main()
