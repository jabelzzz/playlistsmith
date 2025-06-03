import customtkinter
from playlistsmith.ui.screens.login_screen import LoginScreen


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("PlaylistSmith")
        self.iconbitmap("playlistsmith/ui/assets/icon.ico")
        self.geometry("400x180")
        self.grid_columnconfigure(0, weight=1)


try:
    login_screen = LoginScreen()
    login_screen.mainloop()
except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
app = App()
app.mainloop()
