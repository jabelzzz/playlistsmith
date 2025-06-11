import customtkinter

__all__ = ["LoadingScreen"]

class LoadingScreen(customtkinter.CTkFrame):
    def __init__(self, master, message="Loading..."):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        # Configure the grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Container to center the content
        container = customtkinter.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, sticky="ns")

        # Add a loading indicator
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
            width=200
        )
        self.progress.pack(pady=10)
        self.progress.start()

        # Ensure it takes up all the space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def destroy(self):
        # Stop the animation before destroying
        if hasattr(self, 'progress'):
            self.progress.stop()
        super().destroy()
