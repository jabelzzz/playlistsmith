import customtkinter
import os
import platform
from PIL import Image, ImageTk
from playlistsmith.ui.screens.playlist_selection_screen import PlaylistSelectionScreen
from playlistsmith.ui.screens.playlist_detail_screen import PlaylistDetailScreen
from playlistsmith.ui.screens.loading_screen import LoadingScreen

class MainWindow(customtkinter.CTk):
    def __init__(self, spotify_client):
        """Initialize the main application window.
        
        Args:
            spotify_client: An instance of the Spotify client for API interactions.
        """
        super().__init__()
        
        self.spotify_client = spotify_client
        self.title("PlaylistSmith")
        
        # Window configuration
        self.geometry("1000x700")
        self.minsize(1000, 700)
        self.maxsize(1000, 700)
        self.resizable(False, False)
        
        # Load the app icon
        self._load_app_icon()
        
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.current_screen = None
        self.loading_screen = None
        
        # Show the playlist selection screen
        self.show_playlist_selection()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _load_app_icon(self):
        """Load the application icon from the assets directory.
        
        The icon is loaded differently depending on the operating system.
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            icon_path = os.path.join(project_root, "playlistsmith/assets", "ps_icon.ico")
            
            img = Image.open(icon_path)
            
            if platform.system() == 'Windows':
                self.iconbitmap(icon_path)
            else:  # For macOS and Linux
                photo = ImageTk.PhotoImage(img)
                self.tk.call('wm', 'iconphoto', self._w, photo)
                
            print("Application icon loaded successfully")
            
        except Exception as e:
            print(f"Error loading icon: {e}")
            print(f"Error type: {type(e).__name__}")

    def _show_loading(self, message="Loading..."):
        """Display a loading screen with the specified message.
        
        Args:
            message (str): The message to display on the loading screen.
        """
        if self.loading_screen:
            self.loading_screen.destroy()
        self.loading_screen = LoadingScreen(self, message)
        self.loading_screen.grid(row=0, column=0, sticky="nsew")
        self.update()  # Force the UI update

    def _hide_loading(self):
        """Hide the currently displayed loading screen."""
        if self.loading_screen:
            self.loading_screen.destroy()
            self.loading_screen = None

    def _setup_screen(self, screen):
        """Configure and display a new screen.
        
        Args:
            screen: The screen widget to be displayed.
        """
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = screen
        self.current_screen.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_playlist_selection(self):
        """Display the playlist selection screen with a loading indicator."""
        self._show_loading("Loading your playlists...")
        self.after(100, self._load_playlist_selection)

    def _load_playlist_selection(self):
        """Load and display the playlist selection screen."""
        try:
            screen = PlaylistSelectionScreen(self, self.spotify_client)
            self._setup_screen(screen)
        finally:
            self._hide_loading()

    def show_playlist_detail(self, playlist):
        """Display the playlist detail screen for the specified playlist.
        
        Args:
            playlist: The playlist object containing details to display.
        """
        self._show_loading("Loading songs...")
        self.after(100, self._load_playlist_detail, playlist)

    def _load_playlist_detail(self, playlist):
        """Load and display the detail view for a specific playlist.
        
        Args:
            playlist: The playlist object to display details for.
        """
        try:
            screen = PlaylistDetailScreen(
                self,
                playlist,
                self.spotify_client,
                on_back_callback=self.show_playlist_selection
            )
            self._setup_screen(screen)
        finally:
            self._hide_loading()

    def on_closing(self):
        """Handle the window close event by cleaning up resources and exiting the application."""
        print("Closing the application...")
        self.destroy()
        exit()
