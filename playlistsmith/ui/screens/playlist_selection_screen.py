import requests
from io import BytesIO
import os
from PIL import Image
import customtkinter

# Implicit export to evade import problems
__all__ = ["PlaylistSelectionScreen"]

class PlaylistSelectionScreen(customtkinter.CTkFrame):
    def __init__(self, master, spotify_client):
        super().__init__(master)
        self.spotify_client = spotify_client
        self.grid(sticky="nsew")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_playlist_buttons()

    def create_playlist_buttons(self):
        label = customtkinter.CTkLabel(
            self, text="Select a playlist", font=("Arial", 16))
        label.grid(row=0, column=0, pady=20, sticky="n")

        container = customtkinter.CTkScrollableFrame(self)
        container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        for i in range(3):
            container.columnconfigure(i, weight=1)

        playlists = self.spotify_client.current_user_playlists().get('items', [])

        for idx, playlist in enumerate(playlists):
            ctk_img = None
            try:
                if playlist.get('images') and len(playlist['images']) > 0:
                    response = requests.get(
                        playlist['images'][0]['url'], timeout=5)
                    if response.status_code == 200:
                        img = Image.open(BytesIO(response.content)).resize(
                            (64, 64), Image.Resampling.LANCZOS)
                        ctk_img = customtkinter.CTkImage(
                            light_image=img, dark_image=img, size=(64, 64))

                if ctk_img is None:
                    base_dir = os.path.dirname(os.path.dirname(
                        os.path.dirname(os.path.abspath(__file__))))
                    default_image_path = os.path.join(
                        base_dir, "assets", "playlist_default_image.png")
                    if os.path.exists(default_image_path):
                        img = Image.open(default_image_path).resize(
                            (64, 64), Image.Resampling.LANCZOS)
                        ctk_img = customtkinter.CTkImage(
                            light_image=img, dark_image=img, size=(64, 64))

            except Exception as e:
                print(f"Error cargando imagen: {e}")

            btn = customtkinter.CTkButton(
                container,
                text=playlist["name"],
                image=ctk_img,
                fg_color="transparent",
                hover=True,
                compound="left",
                command=lambda playlist=playlist: self.show_playlist_detail(playlist)
            )
            btn.grid(row=idx//3, column=idx % 3, pady=5, padx=5, sticky="nsew")

    def show_playlist_detail(self, playlist_id):
        if hasattr(self.master, 'show_playlist_detail'):
            self.master.show_playlist_detail(playlist_id)
            