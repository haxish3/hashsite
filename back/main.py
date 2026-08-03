import secrets

from config import API_SECRET
from core import get_discord, get_OnoF, get_roblox, get_spotify, get_visits, set_status
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(x_api_key: str | None = Header(default=None)):
    if (
        x_api_key is None
        or API_SECRET is None
        or not secrets.compare_digest(x_api_key, API_SECRET)
    ):
        raise HTTPException(status_code=403, detail="forbidden")


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
    return "In progress..."


@app.post("/toggle", dependencies=[Depends(verify_api_key)])
def _toggle(status: bool):
    return set_status(status)


@app.get("/live")
def _get_live():
    if get_OnoF():
        spotify_data = get_spotify()
        roblox_data = get_roblox()
        return {"spotify": spotify_data, "roblox": roblox_data}

    return {"spotify": {"playing": False}, "roblox": {"online": False}}
