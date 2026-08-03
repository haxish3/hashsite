from datetime import datetime
from pathlib import Path

import requests
from config import ROBLOX_API, ROBLOX_COOKIE, ROBLOX_USER_ID
from requests.exceptions import RequestException

from .spotify import get_color, opacityUpdate
from .supabase import clear_game_session, get_game_session, save_game_session

session_path = Path("data/game_session.json")


def get_img(universeId):
    if not universeId:
        return None

    URL = f"https://thumbnails.roblox.com/v1/games/icons?universeIds={universeId}&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false"

    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("data", [{}])[0].get("imageUrl")
    except RequestException as e:
        print(f"ERROR ROBLOX THUMBNAIL REQUEST: {e}")
    except Exception as e:
        print(f"ERROR ROBLOX THUMBNAIL PARSE: {e}")
    return None


def get_session():
    session = get_game_session()
    if session:
        return session
    return {"gameName": None, "startedAt": None}


def save_session(gameName, startedAt):
    save_game_session({"gameName": gameName, "startedAt": startedAt})


def clear_session():
    clear_game_session()


def get_roblox():
    if not ROBLOX_API or not ROBLOX_COOKIE or not ROBLOX_USER_ID:
        return {"online": False, "error": "missing roblox credentials"}

    try:
        response = requests.post(
            ROBLOX_API,
            json={"userIds": [ROBLOX_USER_ID]},
            cookies={".ROBLOSECURITY": ROBLOX_COOKIE},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except RequestException as e:
        print(f"ERROR ROBLOX REQUEST: {e}")
        return {"online": False, "error": "request failed"}
    except ValueError as e:
        print(f"ERROR ROBLOX JSON: {e}")
        return {"online": False, "error": "invalid response"}

    presence = data.get("userPresences", [{}])[0]
    status = presence.get("userPresenceType")
    gameName = presence.get("lastLocation")
    placeId = presence.get("placeId")
    gameId = presence.get("gameId")
    universeId = presence.get("universeId")

    if placeId:
        link = f"roblox://experiences/start?placeId={placeId}&gameInstanceId={gameId}"
        imageUrl = get_img(universeId)

        session = get_session()

        if session["gameName"] != gameName:
            started = datetime.now().isoformat()
            save_session(gameName, started)
        else:
            started = session.get("startedAt") or datetime.now().isoformat()

        try:
            startTime = datetime.fromisoformat(started)
            elapse = int((datetime.now() - startTime).total_seconds())
        except Exception as e:
            print(f"ERROR ROBLOX SESSION PARSE: {e}")
            elapse = None

        return {
            "online": True,
            "playing": True,
            "game": gameName,
            "image_url": imageUrl,
            "join_link": link,
            "Rcolor": opacityUpdate(get_color(imageUrl)),
            "elapse_sec": elapse,
        }
    if status == 1:
        return {"online": True, "playing": False}

    clear_session()
    return {"online": False}
