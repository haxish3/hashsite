from fastapi import FastAPI
from core import get_roblox, get_spotify, get_discord, get_visit, set_status, get_OnoF
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
    return {"online": True}


@app.get("/api/roblox")
def _roblox():
    if get_OnoF():
        return get_roblox()
    else:
        return {"online": False}


@app.get("/api/spotify")
def _spotify():
    if get_OnoF():
        return get_spotify()
    else:
        return {"playing": False}


@app.get("/api/discord")
def _discord():
    return get_discord()


@app.get("/api/visit")
def _get_visit():
    return get_visit()


@app.get("/api/status")
def _get_all():
    return "mesa"


@app.post("/api/toggle")
def _toggle(status: bool):
    return set_status(status)
