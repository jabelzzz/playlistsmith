import customtkinter
from playlistsmith.services.sort_playlist import PlaylistSorter
# Implicit export to evade import problems
__all__ = ["PlaylistSelectionScreen"]


class PlaylistSelectionScreen(customtkinter.CTkFrame):
    def __init__(self, master, spotify_client, on_playlist_selected):
        super().__init__(master)
        self.spotify_client = spotify_client
        self.on_playlist_selected = on_playlist_selected
        self.grid(sticky="nsew")
        self.create_playlist_buttons()

    # TODO: Finish the playlist buttons function dinamically using the spotify_client.playlists[] 

    def create_playlist_buttons(self):
        playlist = PlaylistSorter
        # Ejemplo de placeholder
        label = customtkinter.CTkLabel(
            self, text="Selecciona una playlist", font=("Arial", 16))
        label.pack(pady=20)
        # Aquí iría la lógica para crear un botón por cada playlist
        # Por ahora, solo un botón de ejemplo
        btn = customtkinter.CTkButton(self, text="Playlist de ejemplo",
                                      command=lambda: self.on_playlist_selected("playlist_id_ejemplo"))
        btn.pack(pady=10)
