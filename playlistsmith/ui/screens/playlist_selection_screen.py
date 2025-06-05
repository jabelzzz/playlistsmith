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

    def create_playlist_buttons(self):
        # TODO: Finish the playlist buttons function dynamically using spotify_client.playlists[]
        label = customtkinter.CTkLabel(
            self, text="Select a playlist", font=("Arial", 16))
        label.pack(pady=20)
        # Here will go the logic to create a button for each playlist
        # For now, just an example button
        btn = customtkinter.CTkButton(self, text="Example playlist",
                                      command=lambda: self.on_playlist_selected("playlist_id_example"))
        btn.pack(pady=10)
