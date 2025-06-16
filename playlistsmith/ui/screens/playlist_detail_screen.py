import customtkinter
from playlistsmith.services.sort_playlist import PlaylistSorter


class PlaylistDetailScreen(customtkinter.CTkFrame):
    """A screen that displays detailed information about a Spotify playlist."""

    def __init__(self, master, playlist, spotify_client, on_back_callback=None):
        """Initialize the playlist detail screen.

        Args:
            master: The parent widget.
            playlist (dict): The playlist data.
            spotify_client: An instance of the Spotify client for API interactions.
            on_back_callback (callable, optional): Function to call when going back.
        """
        super().__init__(master)
        self.playlist = playlist
        self.spotify_client = spotify_client
        self.on_back_callback = on_back_callback
        self.current_sort_frame = None  # To track the current sort frame

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

        self.songs_container = customtkinter.CTkScrollableFrame(self)
        self.songs_container.grid(row=1, column=0, sticky="nsew", padx=0.5)

        # Configure column widths
        column_config = [
            (0, 100),  # Song
            (1, 100),  # Artist
            (2, 100),  # Album
            (3, 80)    # Duration
        ]

        for col, width in column_config:
            self.songs_container.grid_columnconfigure(
                col, weight=1, minsize=width)

        # Frame for sort options
        self.sort_options_container = customtkinter.CTkFrame(self)
        self.sort_options_container.grid(
            row=1, column=1, sticky="nse", padx=(5, 0))

        # Display the header and songs
        self.build_header(self.songs_container)
        self.load_songs(self.songs_container)

        # Display the sort menu
        self.show_sort_menu()

    def build_header(self, container):
        """Build the header row with column titles.

        Args:
            container: The parent widget for the header.
        """
        headers = ["SONG", "ARTIST", "ALBUM", "DURATION"]
        for col, header in enumerate(headers):
            customtkinter.CTkLabel(
                container,
                text=header,
                font=("Arial", 14, "bold"),
                anchor="w"
            ).grid(row=0, column=col, sticky="w", padx=5, pady=(0, 5))

        # Separator line
        customtkinter.CTkFrame(
            container, height=1, fg_color="gray50"
        ).grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 10))

    def load_songs(self, container):
        """Load and display songs from the playlist using PlaylistSorter.

        Args:
            container: The parent widget for the songs list.
        """
        try:
            # Use PlaylistSorter to get all songs
            sorter = PlaylistSorter(self.spotify_client, self.playlist['id'])
            all_tracks = sorter.get_all_tracks()

            # Display the songs
            # Start at 2 for the header
            for idx, track in enumerate(all_tracks, start=2):
                artists = ", ".join([artist["name"]
                                    for artist in track.get("artists", [])])
                duration_str = self.format_duration(
                    track.get("duration_ms", 0))

                data = [
                    track.get("name", "Unknown"),
                    artists,
                    track.get("album", {}).get("name", "Unknown"),
                    duration_str
                ]

                for col, value in enumerate(data):
                    customtkinter.CTkLabel(
                        container,
                        text=value,
                        anchor="w",
                        font=("Arial", 13),
                        text_color=("gray50", "gray70") if col != 0 else None,
                        wraplength=150  # Max for long titles
                    ).grid(row=idx, column=col, sticky="w", padx=10, pady=(0, 5))

        except Exception as e:
            print(f"Error loading songs: {e}")

    def show_sort_menu(self):
        """Display the main sorting options menu."""
        # Clear current container
        for widget in self.sort_options_container.winfo_children():
            widget.destroy()

        # Title
        customtkinter.CTkLabel(
            self.sort_options_container,
            text="Sort By",
            font=("Arial", 13, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="n", padx=10, pady=(0, 10))

        # Sorting options with submenus
        sort_options = [
            ("By Artist", self.show_artist_sort_options),
            ("By Release Date", self.show_release_date_sort_options),
            ("By Duration", self.show_duration_sort_options),
            ("By Popularity", self.show_popularity_sort_options)
        ]

        for i, (text, command) in enumerate(sort_options, start=1):
            btn = customtkinter.CTkButton(
                self.sort_options_container,
                text=text,
                command=command,
                fg_color="#7FFFD4",
                hover_color="#66CDAA",
                text_color="black"
            )
            btn.grid(row=i, column=0, pady=2, padx=5, sticky="ew")

    def create_sort_options_menu(self, title, options):
        """Helper method to create a generic sort options menu.

        Args:
            title (str): Title for the menu
            options (list): List of tuples (text, sort_type)
        """
        # Clear current container
        for widget in self.sort_options_container.winfo_children():
            widget.destroy()

        # Title
        customtkinter.CTkLabel(
            self.sort_options_container,
            text=title,
            font=("Arial", 13, "bold"),
            anchor="w"
        ).grid(row=0, column=0, sticky="n", padx=10, pady=(0, 10))

        # Add sort options
        for i, (text, sort_type) in enumerate(options, start=1):
            btn = customtkinter.CTkButton(
                self.sort_options_container,
                text=text,
                command=lambda st=sort_type: self.sort_playlist(st),
                fg_color="#7FFFD4",  # Aquamarine color
                hover_color="#66CDAA",  # Darker aquamarine on hover
                text_color="black"
            )
            btn.grid(row=i, column=0, pady=2, padx=5, sticky="ew")

        # Back button
        customtkinter.CTkButton(
            self.sort_options_container,
            text="← Back",
            command=self.show_sort_menu,
            fg_color="#7FFFD4",  # Aquamarine color
            hover_color="#66CDAA",  # Darker aquamarine on hover
            text_color="black"
        ).grid(row=len(options)+1, column=0, pady=(10, 5), padx=5, sticky="ew")

    def show_artist_sort_options(self):
        """Show artist sorting options."""
        options = [
            ("A → Z (Ascending)", "artist_asc"),
            ("Z → A (Descending)", "artist_desc")
        ]
        self.create_sort_options_menu("Sort by Artist", options)

    def show_release_date_sort_options(self):
        """Show release date sorting options."""
        options = [
            ("Newest First", "release_desc"),
            ("Oldest First", "release_asc")
        ]
        self.create_sort_options_menu("Sort by Release Date", options)

    def show_duration_sort_options(self):
        """Show duration sorting options."""
        options = [
            ("Longest First", "duration_desc"),
            ("Shortest First", "duration_asc")
        ]
        self.create_sort_options_menu("Sort by Duration", options)

    def show_popularity_sort_options(self):
        """Show popularity sorting options."""
        options = [
            ("Most Popular First", "popularity_desc"),
            ("Least Popular First", "popularity_asc")
        ]
        self.create_sort_options_menu("Sort by Popularity", options)

    def sort_playlist(self, sort_type):
        """Sort the playlist by the specified criteria.

        Args:
            sort_type (str): The type of sorting to apply.
                           Options: 'artist_asc', 'artist_desc', 'release', 'duration', 'popularity'
        """
        try:
            sorter = PlaylistSorter(self.spotify_client, self.playlist["id"])

            if sort_type == "artist_asc":
                sorter.sort_by_artist(reverse=False)
            elif sort_type == "artist_desc":
                sorter.sort_by_artist(reverse=True)
            elif sort_type == "release_desc":
                sorter.sort_by_release_date(reverse=True)
            elif sort_type == "release_asc":
                sorter.sort_by_release_date(reverse=False)
            elif sort_type == "duration_desc":
                sorter.sort_by_duration(reverse=True)
            elif sort_type == "duration_asc":
                sorter.sort_by_duration(reverse=False)
            elif sort_type == "popularity_desc":
                sorter.sort_by_popularity(reverse=True)
            elif sort_type == "popularity_asc":
                sorter.sort_by_popularity(reverse=False)

            # Update the UI after sorting
            self.update_after_sorting()

            # Return to the main menu after sorting
            self.show_sort_menu()

        except Exception as e:
            print(f"Error sorting the playlist: {e}")

    def update_after_sorting(self):
        """Update the UI after sorting the playlist."""
        # Clear current container
        for widget in self.songs_container.winfo_children():
            widget.destroy()

        # Rebuild the songs container
        self.songs_container = customtkinter.CTkScrollableFrame(self)
        self.songs_container.grid(row=1, column=0, sticky="nsew", padx=0.5)

        # Reconfigure the columns
        column_config = [
            (0, 100),  # Song
            (1, 100),  # Artist
            (2, 100),  # Album
            (3, 80)    # Duration
        ]

        for col, width in column_config:
            self.songs_container.grid_columnconfigure(
                col, weight=1, minsize=width)

        # Rebuild the header and load the songs
        self.build_header(self.songs_container)
        self.load_songs(self.songs_container)

        # Force the UI to update
        self.update_idletasks()

    @staticmethod
    def format_duration(ms):
        """Convert milliseconds to MM:SS format.

        Args:
            ms (int): Duration in milliseconds.

        Returns:
            str: Formatted duration string (MM:SS).
        """
        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        return f"{minutes}:{seconds:02}"

    def create_back_button(self):
        """Create and place the back button in the top-left corner."""
        back_btn = customtkinter.CTkButton(
            self, text="← Back", command=self.back_to_playlist_selection,
            fg_color="#7FFFD4",  # Aquamarine color
            hover_color="#66CDAA",  # Darker aquamarine on hover
            text_color="black"
        )
        back_btn.place(x=10, y=10)

    def back_to_playlist_selection(self):
        """Handle the back button click event."""
        if self.on_back_callback:
            callback = self.on_back_callback
            self.destroy()
            callback()
        else:
            self.destroy()
