import customtkinter

class LoadingScreen(customtkinter.CTkFrame):
    """A full-screen loading indicator with a message and progress bar."""
    
    def __init__(self, parent, message="Loading..."):
        """Initialize the loading screen.
        
        Args:
            parent: Parent widget
            message: Message to display while loading
        """
        super().__init__(parent)
        self.parent = parent
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create container frame
        self.container = customtkinter.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Loading message
        self.message_label = customtkinter.CTkLabel(
            self.container,
            text=message,
            font=("Arial", 16)
        )
        self.message_label.pack(pady=(0, 20))
        
        # Progress bar
        self.progress = customtkinter.CTkProgressBar(
            self.container,
            mode="indeterminate",
            fg_color=("gray85", "gray25"),
            progress_color="#7FFFD4",
            width=300
        )
        self.progress.pack(pady=(0, 20))
        self.progress.start()
    
    def set_message(self, message):
        """Update the loading message.
        
        Args:
            message: New message to display
        """
        self.message_label.configure(text=message)
    
    def _on_cancel(self):
        """Handle cancel button click."""
        self.progress.stop()
        self.destroy()
        if hasattr(self.parent, 'on_cancel_loading'):
            self.parent.on_cancel_loading()
