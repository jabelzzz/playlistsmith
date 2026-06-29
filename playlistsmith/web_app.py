import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from playlistsmith.api import router as api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="PlaylistSmith SaaS", version="0.1.0")
app.include_router(api_router)

# Mount static files using absolute path so the server can find assets regardless of cwd
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def index():
    # Redirect to the single-file frontend for testing
    return RedirectResponse(url="/static/index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "playlistsmith"}
