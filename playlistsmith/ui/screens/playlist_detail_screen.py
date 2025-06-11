import customtkinter

class PlaylistDetailScreen(customtkinter.CTkFrame):
    def __init__(self, master, playlist_id, spotify_client, on_back_callback=None):
        super().__init__(master)
        self.playlist_id = playlist_id
        self.spotify_client = spotify_client
        self.on_back_callback = on_back_callback
        self.grid(sticky="nsew")
        self.create_back_button()
        self.show_playlist_songs()

    def create_back_button(self):
        back_btn = customtkinter.CTkButton(
            self, text="← Playlists", command=self.back_to_playlist_selection)
        back_btn.place(x=10, y=10)

    def back_to_playlist_selection(self):
        if self.on_back_callback:
            callback = self.on_back_callback
            self.destroy()
            callback()
        else:
            self.destroy()

    def show_playlist_songs(self):
        label = customtkinter.CTkLabel(
            self, text=f"Playlist Songs: {self.playlist_id}", font=("Arial", 14))
        label.pack(pady=50)
        # TODO: Mostrar las canciones de la playlist