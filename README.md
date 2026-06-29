# 🎵 PlaylistSmith - Spotify Playlist Organizer

**PlaylistSmith** is a web-based Spotify playlist manager powered by FastAPI and a lightweight browser UI. Authenticate with Spotify, browse your playlists, reorder songs by metadata, and remove duplicate tracks without deleting any content.

> 🎧 Smart playlist sorting from your browser.  
> 🚀 Reorder tracks, remove duplicates, and keep your playlist clean.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Spotify-1DB954?logo=spotify&logoColor=white" alt="Spotify">
</p>

## ✨ Key Features

- 🔐 Spotify OAuth authentication
- 🌐 Browser-based UI served from `/static`
- 📄 Browse your Spotify playlists
- 🔀 Reorder playlist tracks by:
  - Artist
  - Release date
  - Duration
  - Popularity
- 🧹 Remove duplicate tracks while keeping the first occurrence
- 🧩 Lightweight FastAPI backend with static frontend support
- 🐳 Docker Compose deployment ready

## 📋 Prerequisites

- A Spotify account (free or premium)
- Internet connection

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jabelzzz/playlistsmith.git
   cd playlistsmith
   ```

2. **Install dependencies**

   Using Pipenv:
   ```bash
   pip install --user pipenv
   pipenv install --dev
   pipenv shell
   ```

   Or with pip directly if you prefer:
   ```bash
   python3 -m pip install --upgrade pip
   python3 -m pip install fastapi uvicorn spotipy python-dotenv
   ```

3. **Configure Spotify credentials**

   Set the required Spotify environment variables in `docker-compose.yml` or in your shell before running Docker Compose.

   Example values to set in `docker-compose.yml`:
   ```yaml
   environment:
     SPOTIPY_CLIENT_ID: your_spotify_client_id
     SPOTIPY_CLIENT_SECRET: your_spotify_client_secret
     SPOTIPY_REDIRECT_URI: http://localhost:8000/callback
     COOKIE_SECURE: false
   ```

   - Register an app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   - Add `http://localhost:8000/callback` as a Redirect URI.

## ▶️ Run locally

Start the application with:
```bash
python3 main.py
```

Then open your browser at `http://127.0.0.1:8000`.

## 🌐 How it works

1. Click **Login with Spotify**.
2. Authorize the app with Spotify.
3. The OAuth callback stores the access token in a server-side session and sets an HTTP-only session cookie.
4. Browse playlists and select one.
5. Sort tracks or remove duplicate songs.

## 🧪 API Endpoints

- `GET /login` — redirect to Spotify authorization
- `GET /callback` — OAuth callback handler
- `GET /playlists` — list current user playlists
- `POST /sort` — reorder playlist tracks
- `POST /remove_duplicates` — remove duplicate tracks from a playlist
- `GET /health` — health check endpoint

## 🐳 Docker deployment

Build and run with Docker Compose:
```bash
docker compose build --pull
docker compose up -d
```

The service listens on port `8000` by default.

Verify the service:
```bash
curl -f http://127.0.0.1:8000/health
```

## 📁 Project Structure

```
playlistsmith/
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── README.md
├── docker-compose.yml
├── main.py
├── playlistsmith/
│   ├── api.py
│   ├── web_app.py
│   ├── static/
│   │   ├── app.js
│   │   ├── index.html
│   │   └── styles.css
│   ├── services/
│   │   ├── sort_playlist.py
│   │   └── spotify_auth.py
│   └── __init__.py
└── tests/
    └── test_playlist_sorter.py
```

## 💡 Notes

- All Spotify credentials and session options must be configured through `docker-compose.yml`.
- The application stores the Spotify access token server-side and does not expose it to browser storage.

## 🤝 Contributing

Contributions are welcome.

1. Fork the project
2. Create a new branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## 📄 License

No license file is included in the repository at this time.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/jabelzzz">Jabel Álvarez</a>
</p>
