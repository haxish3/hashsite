from core import get_roblox, get_spotify, get_discord, get_visit, set_status, get_OnoF
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def _teste():
    return {"online": get_OnoF()}


@app.get("/roblox")
def _roblox():
    if get_OnoF():
        return get_roblox()
    else:
        return {"online": False}


@app.get("/spotify")
def _spotify():
    if get_OnoF():
        return get_spotify()
    else:
        return {"playing": False}


@app.get("/discord")
def _discord():
    return get_discord()


@app.get("/visit")
def _get_visit():
    return get_visit()


@app.get("/status")
def _get_all():
    return "pornhub.com/"


@app.post("/toggle")
def _toggle(status: bool):
    return set_status(status)
