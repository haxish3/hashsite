from config import ROBLOX_COOKIE, ROBLOX_USER_ID, ROBLOX_API
from .spotify import get_color, opacityUpdate
from datetime import datetime, timedelta  # noqa
from pathlib import Path
import requests
import json

session_path = Path("data/game_session.json")


def get_img(universeId):
    URL = f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false"

    resp = requests.get(URL)
    data = resp.json()["data"][0]["imageUrl"]

    return data


def get_session():
    if session_path.exists():
        with session_path.open("r") as f:
            return json.load(f)
    return {"gameId": 0, "startedAt": 0}


def save_session(gameId, startedAt):
    with session_path.open("w") as f:
        save = {"gameId": gameId, "startedAt": startedAt}
        json.dump(save, f)


def clear_session():
    save_session(None, None)


def get_roblox():
    response = requests.post(
        ROBLOX_API,
        json={"userIds": [ROBLOX_USER_ID]},
        cookies={".ROBLOSECURITY": ROBLOX_COOKIE},
    )

    data = response.json()

    status = data["userPresences"][0]["userPresenceType"]
    gameName = data["userPresences"][0]["lastLocation"]
    placeId = data["userPresences"][0]["placeId"]
    gameId = data["userPresences"][0]["gameId"]
    universeId = data["userPresences"][0]["universeId"]

    if placeId:
        link = f"roblox://experiences/start?placeId={placeId}&gameInstanceId={gameId}"
        imageUrl = get_img(universeId)

        session = get_session()

        if session["gameId"] != gameId:
            started = datetime.now().isoformat()
            save_session(gameId, started)
        else:
            started = session["startedAt"]

        startTime = datetime.fromisoformat(started)
        elapse = int((datetime.now() - startTime).total_seconds())

        return {
            "online": True,
            "playing": True,
            "game": gameName,
            "image_url": imageUrl if imageUrl else None,
            "join_link": link,
            "Rcolor": opacityUpdate(get_color(imageUrl)),
            "elapse_sec": elapse if elapse else None,
        }
    elif status == 1:
        return {"online": True, "playing": False}
    elif status == 0:
        return {"online": False}
