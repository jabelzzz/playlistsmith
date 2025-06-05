import customtkinter
from playlistsmith.ui.screens.playlist_selection_screen import PlaylistSelectionScreen
from playlistsmith.ui.screens.playlist_detail_screen import PlaylistDetailScreen


class MainWindow(customtkinter.CTk):
    def __init__(self, spotify_client):
        super().__init__()
        self.spotify_client = spotify_client
        self.title("PlaylistSmith")
        self.iconbitmap("playlistsmith/assets/ps_icon.ico")
        self.geometry("800x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.current_screen = None
        self.show_playlist_selection()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def show_playlist_selection(self):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = PlaylistSelectionScreen(
            self, self.spotify_client, self.show_playlist_detail)

    def show_playlist_detail(self, playlist_id):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = PlaylistDetailScreen(
            self, playlist_id, self.spotify_client, self.show_playlist_selection)

    def on_closing(self):
        print("Closing the application...")
        self.destroy()
        exit()
