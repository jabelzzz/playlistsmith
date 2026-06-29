"""API layer for PlaylistSmith SaaS.

This module exposes FastAPI endpoints for:
- /login -> starts Spotify OAuth flow
- /callback -> receives Spotify OAuth callback
- /playlists -> list user playlists
- /sort -> reorder a playlist using existing sorting logic

Each endpoint delegates to functions in `playlistsmith.services`.
"""
import json
import os
import time
from uuid import uuid4

import spotipy
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from spotipy.oauth2 import SpotifyOAuth

from playlistsmith.services.sort_playlist import PlaylistSorter

router = APIRouter()

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() in ("1", "true", "yes")
SESSION_STORE: dict[str, dict] = {}


def get_sp_oauth():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
    missing = [name for name, value in (
        ("SPOTIPY_CLIENT_ID", client_id),
        ("SPOTIPY_CLIENT_SECRET", client_secret),
        ("SPOTIPY_REDIRECT_URI", redirect_uri),
    ) if not value]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Spotify credentials missing: {', '.join(missing)}"
        )
    return SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                        scope="user-library-read playlist-modify-public playlist-modify-private")


@router.get("/login")
def login(sp_oauth: SpotifyOAuth = Depends(get_sp_oauth)):
    """Redirect the user to Spotify authorization page."""
    auth_url = sp_oauth.get_authorize_url(show_dialog=True)
    return RedirectResponse(auth_url)


@router.get("/callback")
def callback(request: Request, sp_oauth: SpotifyOAuth = Depends(get_sp_oauth)):
    """Handle Spotify redirect and store the token in a server-side session cookie."""
    code = request.query_params.get("code")
    if not code:
        return JSONResponse({"error": "No code provided"}, status_code=400)

    try:
        token_info = sp_oauth.get_access_token(code)
    except Exception as exc:
        return JSONResponse({"error": "Failed to obtain access token", "detail": str(exc)}, status_code=500)

    access_token = token_info.get("access_token") if token_info else None
    if not access_token:
        return JSONResponse({"error": "Failed to obtain access token", "detail": token_info}, status_code=500)

    if "expires_at" not in token_info and token_info.get("expires_in"):
        token_info["expires_at"] = int(time.time()) + int(token_info["expires_in"])

    session_id = str(uuid4())
    SESSION_STORE[session_id] = token_info

    response = RedirectResponse(url="/")
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="strict",
        max_age=token_info.get("expires_in", 3600),
        path="/",
    )
    return response


def _get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if session_id not in SESSION_STORE:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return session_id


def _get_spotify_client(request: Request):
    session_id = _get_session_id(request)
    token_info = SESSION_STORE[session_id]
    expires_at = token_info.get("expires_at")

    if expires_at and int(time.time()) > expires_at - 60:
        sp_oauth = get_sp_oauth()
        refresh_token = token_info.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Session expired")

        new_token_info = sp_oauth.refresh_access_token(refresh_token)
        if "refresh_token" not in new_token_info:
            new_token_info["refresh_token"] = refresh_token
        if "expires_at" not in new_token_info and new_token_info.get("expires_in"):
            new_token_info["expires_at"] = int(time.time()) + int(new_token_info["expires_in"])

        SESSION_STORE[session_id] = new_token_info
        token_info = new_token_info

    return spotipy.Spotify(auth=token_info["access_token"])


@router.get("/auth/status")
def auth_status(request: Request):
    _get_session_id(request)
    return {"authenticated": True}


@router.post("/logout")
def logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id:
        SESSION_STORE.pop(session_id, None)
    response = JSONResponse({"status": "ok"})
    response.delete_cookie("session_id", path="/")
    return response


@router.get("/playlists")
def list_playlists(request: Request):
    """Return current user's playlists using the server-side Spotify session."""
    sp = _get_spotify_client(request)
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
    sp = _get_spotify_client(request)
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
    sp = _get_spotify_client(request)
    sorter = PlaylistSorter(sp, payload.playlist_id)
    sorter.remove_duplicates()
    return {"status": "ok"}
