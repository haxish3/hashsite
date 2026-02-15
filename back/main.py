from core import get_roblox, get_spotify, get_discord, get_visits, set_status, get_OnoF
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


@app.get("/discord")
def _discord():
    return get_discord()


@app.get("/visit")
def _get_visit():
    return get_visits()


@app.get("/status")
def _get_all():
    return "pornhub.com/"


@app.post("/toggle")
def _toggle(status: bool):
    return set_status(status)


@app.get("/live")
def _get_live():
    if get_OnoF():
        return {"spotify": get_spotify(), "roblox": get_roblox()}
    return {"spotify": {"playing": False}, "roblox": {"online": False}}
