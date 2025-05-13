import customtkinter

def launch_app():
    """Launch the main application window."""
    # Set the appearance mode and color theme
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    # Create the main application window
    app = customtkinter.CTk()
    app.geometry("800x600")
    app.title("PlaylistSmith")

    # Start the application
    app.mainloop()