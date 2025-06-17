import customtkinter
from playlistsmith.services.spotify_auth import authenticate_spotify

class LoginScreen(customtkinter.CTkFrame):
    """Login screen for Spotify authentication."""
    
    def __init__(self, parent):
        """Initialize the login screen with UI elements."""
        super().__init__(parent)
        self.parent = parent

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Welcome message
        self.label = customtkinter.CTkLabel(
            self,
            text="Welcome to PlaylistSmith\n\nSign in with Spotify to continue", 
            font=("Arial", 16),
            justify="center"
        )
        self.label.grid(row=0, column=0, padx=20, pady=(40, 20))

        # Login button
        self.login_button = customtkinter.CTkButton(
            self,
            text="Sign in with Spotify",
            command=self.login,
            font=("Arial", 14),
            height=40,
            width=200
        )
        self.login_button.grid(row=1, column=0, padx=20, pady=10)

        # Status label
        self.status_label = customtkinter.CTkLabel(
            self,
            text="",
            text_color="gray"
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=10)

    def login(self):
        """Handle login button click event."""
        self.login_button.configure(state="disabled")
        self.status_label.configure(text="Connecting to Spotify...", text_color="white")
        
        # Use after to prevent UI freezing
        self.after(100, self._perform_authentication)
    
    def _perform_authentication(self):
        """Perform Spotify authentication."""
        try:
            spotify_client = authenticate_spotify()
            if spotify_client:
                self.status_label.configure(
                    text="Authentication successful!", 
                    text_color="lightgreen"
                )
                # Notify parent about successful login
                if hasattr(self.parent, 'on_login_success'):
                    self.parent.after(1000, lambda: self.parent.on_login_success(spotify_client))
            else:
                self.status_label.configure(
                    text="Authentication failed. Please try again.", 
                    text_color="#ff6b6b"
                )
                self.login_button.configure(state="normal")
                
        except Exception as e:
            self.status_label.configure(
                text=f"Error: {str(e)}", 
                text_color="#ff6b6b"
            )
            self.login_button.configure(state="normal")