# 🎵 PlaylistSmith - Your Spotify Playlist Manager

**PlaylistSmith** is a desktop application that allows you to manage and organize your Spotify playlists in a simple and intuitive way. With a modern and user-friendly interface, you can sort your favorite songs based on different criteria.

> 🎧 Tired of disorganized playlists?  
> 🔥 Turn chaos into order with PlaylistSmith!

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Spotify-1DB954?logo=spotify&logoColor=white" alt="Spotify">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
</p>

## ✨ Key Features

- 🔐 Secure authentication with your Spotify account
- 🎵 View all your playlists
- 🧠 Sort by multiple criteria:
  - Artist (A-Z / Z-A)
  - Release date (newest / oldest)
  - Duration (longest / shortest)
  - Popularity (most / least popular)
- 🖥️ Modern and responsive graphical interface
- 💾 100% local: your data stays on your computer
- 🚀 Fast and lightweight

## 📋 Prerequisites

- Python 3.10 or higher
- A Spotify account (free or premium)
- Internet connection

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jabelzzz/playlistsmith.git
   cd playlistsmith
   ```

2. **Create a virtual environment**

   Using Pipenv (recommended for development):
   ```bash
   # Install pipenv if you don't have it
   pip install --user pipenv
   
   # Create and activate the virtual environment
   pipenv --python 3.10  # Make sure to use the Python >=3.10
   pipenv shell  # Activate the virtual environment
   ```

3. **Install dependencies**

   ```bash
   pipenv install --dev
   ```
   
   This will install all the necessary dependencies, including development ones.

4. **Set up Spotify credentials**
   - Create an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Add `http://127.0.0.1:8888/callback` as a Redirect URI in your app settings (You can use other port if you want)
   ![Texto alternativo](playlistsmith/assets/redirect_uri.png)
   - Create a `config.env` file in the project root with:
     ```
     SPOTIPY_CLIENT_ID=your_client_id
     SPOTIPY_CLIENT_SECRET=your_client_secret
     SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
     ```
     - You can find you Client_ID and Client_secret at the start of the app
      ![Client IDs](playlistsmith/assets/client_ids.png)
     
## 🎮 How to Use

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Log in with Spotify**
   - Click on "Login with Spotify"
   - Your browser will open to authorize the application
   - Once authorized, you'll be redirected back to the application

3. **Select a playlist**
   - You'll see all your Spotify playlists
   - Click on the one you want to organize

4. **Sort your songs**
   - Use the buttons on the right to sort by:
     - Artist (A-Z)
     - Release date
     - Duration
     - Popularity

## 🛠️ Technologies Used

- **Language**: Python 3.10+
- **GUI Framework**: CustomTkinter
- **Spotify API**: Spotipy
- **Image Handling**: Pillow (PIL)
- **Environment Variables**: python-dotenv
- **Dependency Management**: Pipenv

## 📁 Project Structure

```
playlistsmith/
├── playlistsmith/           # Source code
│   ├── assets/              # Graphical resources (icons, images)
│   ├── services/            # Business logic
│   │   ├── sort_playlist.py # Playlist sorting
│   │   └── spotify_auth.py  # Spotify authentication
│   ├── ui/                  # User interface
│   │   ├── screens/         # Application screens
│   │   └── main_window.py   # Main window
│   └── __init__.py
├── .env.example             # Configuration example
├── Pipfile                  # Dependencies (Pipenv)
├── Pipfile.lock             # Lock file for reproducible builds
└── main.py                  # Entry point
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- To Spotify for their excellent API
- To the developers of the open-source libraries used
- To you, for using PlaylistSmith 🎵

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/jabelzzz">Jabel Álvarez</a>
</p>
