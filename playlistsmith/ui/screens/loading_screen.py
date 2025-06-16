import customtkinter

__all__ = ["LoadingScreen"]

class LoadingScreen(customtkinter.CTkFrame):
    """A full-screen loading indicator with a message and progress bar."""
    
    def __init__(self, master, message="Loading..."):
        """Initialize the loading screen.
        
        Args:
            master: The parent widget.
            message (str, optional): The message to display. Defaults to "Loading...".
        """
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        # Configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container to center the content
        container = customtkinter.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="ns")

        # Add a loading label with the message
        self.loading_label = customtkinter.CTkLabel(
            container,
            text=message,
            font=("Arial", 16)
        )
        self.loading_label.pack(pady=20)

        # Add an indeterminate progress bar
        self.progress = customtkinter.CTkProgressBar(
            container,
            mode="indeterminate",
            width=200,
            fg_color=("gray85", "gray25"),  # Light gray in light mode, dark gray in dark mode
            progress_color="#7FFFD4"
        )
        self.progress.pack(pady=10)
        self.progress.start()

        # Ensure it takes up all the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def destroy(self):
        """Stop the progress animation and destroy the widget.
        
        Overrides the default destroy method to ensure proper cleanup.
        """
        if hasattr(self, 'progress'):
            self.progress.stop()
        super().destroy()
