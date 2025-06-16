import requests
from io import BytesIO
import os
from PIL import Image
import customtkinter

# Implicit export to avoid import problems
__all__ = ["PlaylistSelectionScreen"]

class PlaylistSelectionScreen(customtkinter.CTkFrame):
    """A screen that displays a grid of the user's Spotify playlists for selection."""
    
    def __init__(self, master, spotify_client):
        """Initialize the playlist selection screen.
        
        Args:
            master: The parent widget.
            spotify_client: An instance of the Spotify client for API interactions.
        """
        super().__init__(master)
        self.spotify_client = spotify_client
        self.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_playlist_buttons()

    def create_playlist_buttons(self):
        """Create and display a grid of playlist buttons with their cover art."""
        label = customtkinter.CTkLabel(
            self, text="Select a playlist", font=("Arial", 16))
        label.grid(row=0, column=0, pady=20, sticky="n")

        container = customtkinter.CTkScrollableFrame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Configure 3 columns for the grid
        for i in range(3):
            container.columnconfigure(i, weight=1)

        # Get user's playlists
        playlists = self.spotify_client.current_user_playlists().get('items', [])

        # Create a button for each playlist
        for idx, playlist in enumerate(playlists):
            ctk_img = self._load_playlist_image(playlist)
            
            # Create playlist button
            btn = customtkinter.CTkButton(
                container,
                text=playlist["name"],
                image=ctk_img,
                hover=True,
                compound="left",
                fg_color="transparent",
                hover_color="#7FFFD4",
                text_color="white",
                command=lambda p=playlist: self.show_playlist_detail(p)
            )
            btn.grid(row=idx//3, column=idx % 3, pady=5, padx=5, sticky="nsew")
    
    def _load_playlist_image(self, playlist):
        """Load playlist cover art from URL or use default image.
        
        Args:
            playlist (dict): The playlist data.
            
        Returns:
            CTkImage: The playlist image or None if loading fails.
        """
        try:
            # Try to load from playlist images first
            if playlist.get('images') and len(playlist['images']) > 0:
                response = requests.get(
                    playlist['images'][0]['url'], 
                    timeout=5
                )
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content)).resize(
                        (64, 64), 
                        Image.Resampling.LANCZOS
                    )
                    return customtkinter.CTkImage(
                        light_image=img, 
                        dark_image=img, 
                        size=(64, 64)
                    )

            # Fall back to default image
            base_dir = os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))
            default_image_path = os.path.join(
                base_dir, "assets", "playlist_default_image.png")
                
            if os.path.exists(default_image_path):
                img = Image.open(default_image_path).resize(
                    (64, 64), 
                    Image.Resampling.LANCZOS
                )
                return customtkinter.CTkImage(
                    light_image=img, 
                    dark_image=img, 
                    size=(64, 64)
                )
                
        except Exception as e:
            print(f"Error loading image: {e}")
            
        return None

    def show_playlist_detail(self, playlist):
        """Handle playlist selection and show its details.
        
        Args:
            playlist (dict): The selected playlist data.
        """
        if hasattr(self.master, 'show_playlist_detail'):
            self.master.show_playlist_detail(playlist)