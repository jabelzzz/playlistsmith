import customtkinter
from playlistsmith.services.sort_playlist import PlaylistSorter

# Implicit export to evade import problems
__all__ = ["PlaylistDetailScreen"]


class PlaylistDetailScreen(customtkinter.CTkFrame):
    def __init__(self, master, playlist_id, spotify_client, on_back):
        super().__init__(master)
        self.playlist_id = playlist_id
        self.spotify_client = spotify_client
        self.on_back = on_back
        self.grid(sticky="nsew")
        self.create_back_button()

    def create_back_button(self):
        back_btn = customtkinter.CTkButton(
            self, text="← Playlists", command=self.on_back)
        back_btn.place(x=10, y=10)

    # TODO: Finish the table to show the playlist songs
    def show_playlist_songs(self):
        # Placeholder para la tabla de canciones
        label = customtkinter.CTkLabel(
            self, text=f"Playlist Songs: {self.playlist_id}", font=("Arial", 14))
        label.pack(pady=50)
        # Aquí iría la tabla y los métodos de ordenación
