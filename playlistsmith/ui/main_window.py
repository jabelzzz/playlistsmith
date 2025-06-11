import customtkinter
from playlistsmith.ui.screens.playlist_selection_screen import PlaylistSelectionScreen
from playlistsmith.ui.screens.playlist_detail_screen import PlaylistDetailScreen
from playlistsmith.ui.screens.loading_screen import LoadingScreen


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
        self.loading_screen = None
        self.show_playlist_selection()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _show_loading(self, message="Loading..."):
        """Show the loading screen"""
        if self.loading_screen:
            self.loading_screen.destroy()
        self.loading_screen = LoadingScreen(self, message)
        self.loading_screen.grid(row=0, column=0, sticky="nsew")
        self.update()  # Forzar la actualización de la interfaz

    def _hide_loading(self):
        """Hide the loading screen"""
        if self.loading_screen:
            self.loading_screen.destroy()
            self.loading_screen = None

    def _setup_screen(self, screen):
        """Configure and show the new screen"""
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_playlist_selection(self):
        """Show the playlist selection screen with loading screen"""
        self._show_loading("Loading your playlists...")
        
        # Simulate an asynchronous load
        self.after(100, self._load_playlist_selection)
    
    def _load_playlist_selection(self):
        """Load the playlist selection screen after showing the loading screen"""
        try:
            screen = PlaylistSelectionScreen(self, self.spotify_client)
            self._setup_screen(screen)
        finally:
            self._hide_loading()

    def show_playlist_detail(self, playlist_id):
        """Show the playlist detail screen with loading screen"""
        self._show_loading("Loading the playlist...")
        
        # Simulate an asynchronous load
        self.after(100, self._load_playlist_detail, playlist_id)
    
    def _load_playlist_detail(self, playlist_id):
        """Load the playlist detail screen after showing the loading screen"""
        try:
            screen = PlaylistDetailScreen(
                self,
                playlist_id,
                self.spotify_client,
                on_back_callback=self.show_playlist_selection
            )
            self._setup_screen(screen)
        finally:
            self._hide_loading()

    def on_closing(self):
        """Handle window closing event"""
        print("Closing the application...")
        self.destroy()
        exit()
