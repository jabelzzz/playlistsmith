import customtkinter
from playlistsmith.services.sort_playlist import PlaylistSorter


class PlaylistDetailScreen(customtkinter.CTkFrame):
    def __init__(self, master, playlist, spotify_client, on_back_callback=None):
        super().__init__(master)
        self.playlist = playlist
        self.spotify_client = spotify_client
        self.on_back_callback = on_back_callback

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid(sticky="nsew", padx=10, pady=10)

        self.create_back_button()

        label = customtkinter.CTkLabel(
            self,
            text=f"Playlist: {self.playlist['name']}",
            font=("Arial", 16, "bold")
        )
        label.grid(row=0, column=0, pady=(40, 20), sticky="nw")

        songs_container = customtkinter.CTkScrollableFrame(self)
        songs_container.grid(row=1, column=0, sticky="nsew", padx=(0, 20))  # <-- espacio a la derecha
        songs_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Sort options frame
        sort_options_container = customtkinter.CTkFrame(self)
        sort_options_container.grid(row=1, column=1, sticky="nsew", padx=(20, 0))  # <-- espacio a la izquierda

        self.build_header(songs_container)
        self.load_songs(songs_container)
        self.sort_option_frame(sort_options_container)

    def build_header(self, container):
        headers = ["SONG", "ARTIST", "ALBUM", "Duration"]
        for col, header in enumerate(headers):
            customtkinter.CTkLabel(
                container, text=header,
                font=("Arial", 12, "bold"), anchor="w"
            ).grid(row=0, column=col, sticky="w", padx=10, pady=(0, 10))

        # Separator line
        customtkinter.CTkFrame(
            container, height=1, fg_color="gray50"
        ).grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))

    def load_songs(self, container):
        songs = self.spotify_client.playlist_items(
            self.playlist['id']).get('items', [])

        for idx, song in enumerate(songs, start=2):
            track = song["track"]
            artists = ", ".join([artist["name"]
                                for artist in track["artists"]])
            duration_str = self.format_duration(track["duration_ms"])

            data = [
                track["name"],
                artists,
                track["album"]["name"],
                duration_str
            ]

            for col, value in enumerate(data):
                customtkinter.CTkLabel(
                    container,
                    text=value,
                    anchor="w",
                    font=("Arial", 11),
                    text_color=("gray50", "gray70") if col != 0 else None,
                    wraplength=250  # Max for long tittles
                ).grid(row=idx, column=col, sticky="w", padx=10, pady=(0, 5))

    def sort_playlist(self, sort_type):
        sorter = PlaylistSorter(self.spotify_client, self.playlist["id"])

        if sort_type == "artist":
            sorter.sort_by_artist(reverse=False)
        elif sort_type == "release":
            sorter.sort_by_release_date(reverse=True)
        elif sort_type == "duration":
            sorter.sort_by_duration(reverse=True)
        elif sort_type == "popularity":
            sorter.sort_by_popularity(reverse=True)

        # Recargar la pantalla tras ordenar
        self.update()

    def sort_option_frame(self, container):
        customtkinter.CTkLabel(
            container, text="Sort By",
            font=("Arial", 12, "bold"), anchor="w"
        ).grid(row=0, column=0, sticky="n", padx=10, pady=(0, 10))

        # Botón Sort by Artist
        artist_btn = customtkinter.CTkButton(
            container, text="By Artist (A-Z)", command=lambda: self.sort_playlist("artist"))
        artist_btn.grid(row=1, column=0, pady=5, padx=5)

        # Botón Sort by Release Date
        release_btn = customtkinter.CTkButton(
            container, text="By Release Date (Newest)", command=lambda: self.sort_playlist("release"))
        release_btn.grid(row=2, column=0, pady=5, padx=5)

        # Botón Sort by Duration
        duration_btn = customtkinter.CTkButton(
            container, text="By Duration (Longest)", command=lambda: self.sort_playlist("duration"))
        duration_btn.grid(row=3, column=0, pady=5, padx=5)

        # Botón Sort by Popularity
        popularity_btn = customtkinter.CTkButton(
            container, text="By Popularity (Most)", command=lambda: self.sort_playlist("popularity"))
        popularity_btn.grid(row=4, column=0, pady=5, padx=5)

    def format_duration(self, ms):
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        return f"{minutes}:{seconds:02}"

    def create_back_button(self):
        back_btn = customtkinter.CTkButton(
            self, text="← Back", command=self.back_to_playlist_selection)
        back_btn.place(x=10, y=10)

    def back_to_playlist_selection(self):
        if self.on_back_callback:
            callback = self.on_back_callback
            self.destroy()
            callback()
        else:
            self.destroy()
