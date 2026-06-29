"""API layer for PlaylistSmith SaaS.

This module exposes FastAPI endpoints for:
- /login -> starts Spotify OAuth flow
- /callback -> receives Spotify OAuth callback
- /playlists -> list user playlists
- /sort -> reorder a playlist using existing sorting logic

Each endpoint delegates to functions in `playlistsmith.services`.
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from dotenv import load_dotenv
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pydantic import BaseModel

from playlistsmith.services.sort_playlist import PlaylistSorter

router = APIRouter()

load_dotenv("config.env")


def get_sp_oauth():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    if not all([client_id, client_secret, redirect_uri]):
        raise HTTPException(status_code=500, detail="Spotify credentials missing")
    return SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                        scope="user-library-read playlist-modify-public playlist-modify-private")


@router.get("/login")
def login(sp_oauth: SpotifyOAuth = Depends(get_sp_oauth)):
    """Redirect the user to Spotify authorization page."""
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(request: Request, sp_oauth: SpotifyOAuth = Depends(get_sp_oauth)):
        """Handle Spotify redirect and return a small HTML page that stores the access token in sessionStorage.

        This avoids storing any user tokens on the server and keeps them only in the user's browser session.
        """
        code = request.query_params.get("code")
        if not code:
                return JSONResponse({"error": "No code provided"}, status_code=400)
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info.get("access_token") if token_info else None
        if not access_token:
                return JSONResponse({"error": "Failed to obtain access token"}, status_code=500)

        # Safely embed token into JS using json.dumps
        token_js = json.dumps(access_token)
        html = f"""
        <!doctype html>
        <html>
            <head><meta charset="utf-8"><title>PlaylistSmith - Callback</title></head>
            <body>
                <script>
                    // Store token only in browser sessionStorage and redirect back to app
                    sessionStorage.setItem('spotify_token', {token_js});
                    window.location = '/';
                </script>
                <p>If you are not redirected, <a href="/">click here</a>.</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html)


def _extract_bearer_token(request: Request):
    auth = request.headers.get('authorization') or request.headers.get('Authorization')
    if not auth:
        raise HTTPException(status_code=401, detail="Not authenticated")
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == 'bearer':
        return parts[1]
    raise HTTPException(status_code=400, detail="Invalid authorization header")


@router.get("/playlists")
def list_playlists(request: Request):
    """Return current user's playlists using the Bearer token provided by the client."""
    token = _extract_bearer_token(request)
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playlists(limit=50)
    playlists = []
    for p in results["items"]:
        images = p.get("images") or []
        image_url = images[0]["url"] if images else None
        playlists.append({
            "id": p["id"],
            "name": p["name"],
            "tracks": p["tracks"]["total"],
            "image_url": image_url,
        })
    return {"items": playlists}


class SortRequest(BaseModel):
    playlist_id: str
    method: str = "artist"
    direction: str = "descending"


@router.post("/sort")
def sort_playlist(payload: SortRequest, request: Request):
    """Reorder the given playlist using PlaylistSorter.

    Expects JSON body: {"playlist_id": "id", "method": "artist", "direction": "ascending"|"descending"}
    """
    token = _extract_bearer_token(request)
    sp = spotipy.Spotify(auth=token)
    sorter = PlaylistSorter(sp, payload.playlist_id)
    reverse = payload.direction.lower() == "descending"
    if payload.method == "artist":
        sorter.sort_by_artist(reverse=reverse)
    elif payload.method == "release":
        sorter.sort_by_release_date(reverse=reverse)
    elif payload.method == "duration":
        sorter.sort_by_duration(reverse=reverse)
    elif payload.method == "popularity":
        sorter.sort_by_popularity(reverse=reverse)
    else:
        raise HTTPException(status_code=400, detail="Unknown method")
    return {"status": "ok"}


class RemoveDuplicatesRequest(BaseModel):
    playlist_id: str


@router.post("/remove_duplicates")
def remove_duplicates(payload: RemoveDuplicatesRequest, request: Request):
    """Remove duplicate tracks from a playlist while preserving the first occurrence."""
    token = _extract_bearer_token(request)
    sp = spotipy.Spotify(auth=token)
    sorter = PlaylistSorter(sp, payload.playlist_id)
    sorter.remove_duplicates()
    return {"status": "ok"}
