from .supabase import get_music_history, save_music_history
from config import SPOTIFY_CLIENT, SPOTIFY_SECRET
from colorthief import ColorThief
from io import BytesIO
import requests
import base64
import os


REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")


def get_color(imgURL):
    try:
        resp = requests.get(imgURL)
        img = BytesIO(resp.content)
        color_thief = ColorThief(img)
        cor = color_thief.get_color(quality=10)
        return f"{cor[0]}, {cor[1]}, {cor[2]}"
    except Exception as e:
        print(f"ERROR SPOT COLOR: {e}")
        return "30, 30, 30"


def opacityUpdate(rgb):
    r, g, b = rgb.split(",")
    lumin = 0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b)

    opc = 0.25
    opacity = opc - (lumin / 255) * 0.22
    opacity = max(0.08, min(opc, opacity))

    return f"rgba({r}, {g}, {b}, {opacity:.2f})"


def get_access_token():
    auth = base64.b64encode(f"{SPOTIFY_CLIENT}:{SPOTIFY_SECRET}".encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN},
    )

    data = response.json()

    if "access_token" not in data:
        print(f"ERRO SPOTIFY: {data}")
        return None

    return data["access_token"]


def get_spotify():
    token = get_access_token()

    if not token:
        return {"playing": False, "error": "token failure"}

    response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200 or not response.content:
        track = {"is_playing": False}
    else:
        track = response.json()
        item = track["item"]

    if track["is_playing"]:
        try:
            save_music_history(
                {
                    "track": item["name"],
                    "artist": item["artists"][0]["name"],
                    "album_cover": item["album"]["images"][0]["url"],
                    "track_url": item["external_urls"]["spotify"],
                }
            )
            history_saved = True
        except Exception as e:
            history_saved = False
            print(f"ERROR SPOT: DONT SAVED HISTORY --- {e}")
    else:
        history = get_music_history()
        if history:
            return {
                "playing": False,
                "has_history": True,
                "track": history["track"],
                "artist": history["artist"],
                "album_cover": history["album_cover"],
                "track_url": history["track_url"],
                "color": "rgba(0, 0, 0, 0)",
            }
        return {"playing": False, "has_history": False}

    return {
        "playing": True,
        "history_saved": history_saved,
        "track": item["name"],
        "artist": item["artists"][0]["name"],
        "album_cover": item["album"]["images"][0]["url"],
        "track_url": item["external_urls"]["spotify"],
        "progress": {
            "current": track["progress_ms"] // 1000,
            "total": item["duration_ms"] // 1000,
        },
        "color": opacityUpdate(get_color(item["album"]["images"][0]["url"])),
    }
