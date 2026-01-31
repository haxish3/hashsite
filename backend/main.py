from fastapi import FastAPI
from core import get_roblox, get_spotify, get_discord, get_visit
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
def _teste():
    return {"Online": True}


@app.get("/api/roblox")
def _roblox():
    return get_roblox()


@app.get("/api/spotify")
def _spotify():
    return get_spotify()


@app.get("/api/discord")
def _discord():
    return get_discord()


@app.get("/api/visit")
def _get_visit():
    return get_visit()


@app.get("/api/status")
def _get_all():
    spotify = get_spotify().get("playing")
    roblox = get_roblox().get("online")
    print(roblox, spotify)

    online = spotify or roblox

    return {
        "online": online,
        "activity": "roblox" if roblox else "spotify" if spotify else None,
    }
