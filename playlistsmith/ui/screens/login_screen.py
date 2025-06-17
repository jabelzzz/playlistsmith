import customtkinter
from playlistsmith.services.spotify_auth import authenticate_spotify


class LoginScreen(customtkinter.CTkFrame):
    """Login screen for Spotify authentication."""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self.content_frame = customtkinter.CTkFrame(
            self, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(
            self.content_frame,
            text="Welcome to PlaylistSmith\n\nSign in with Spotify to continue",
            font=("Arial", 16),
            justify="center"
        )
        self.label.grid(row=0, column=0, padx=20, pady=(0, 30))

        self.login_button = customtkinter.CTkButton(
            self.content_frame,
            text="Sign in with Spotify",
            command=self.login,
            font=("Arial", 14),
            fg_color="#7FFFD4",
            hover_color="#66CDAA",
            text_color="black",
            height=40,
            width=200
        )
        self.login_button.grid(row=1, column=0, pady=(0, 20))

        self.status_label = customtkinter.CTkLabel(
            self.content_frame,
            text="",
            text_color="gray"
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=10)

    def login(self):
        """Handle login button click event."""
        self.login_button.configure(state="disabled")
        self.status_label.configure(
            text="Connecting to Spotify...", text_color="white")

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
                    self.parent.after(
                        1000, lambda: self.parent.on_login_success(spotify_client))
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
