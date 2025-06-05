import customtkinter
from playlistsmith.services.spotify_auth import authenticate_spotify
__all__ = ["LoginScreen"]


class LoginScreen(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.title("PlaylistSmith")
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.label = customtkinter.CTkLabel(
            self, text="Please log in Spotify to continue", font=("Arial", 16)
        )
        self.label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.login_button = customtkinter.CTkButton(
            self,
            text="Login",
            command=self.login,
        )
        self.login_button.grid(row=3, column=0, padx=20, pady=(10, 20))

    def login(self):
        print("Login button clicked")
        spotify_client = authenticate_spotify()
        print("Spotify client:", spotify_client)
        if spotify_client:
            print("Spotify authentication successful, proceeding to main window")
            self.destroy()
        else:
            print("Spotify authentication failed")

    def on_closing(self):
        print("Cerrando la aplicación...")
        self.destroy()  # Cierra la ventana
        exit()  # Termina el programa
