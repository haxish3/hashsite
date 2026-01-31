from io import BytesIO
import requests
import base64
import os
from colorthief import ColorThief
from config import SPOTIFY_CLIENT, SPOTIFY_SECRET

SCOPE_READ = "user-read-currently-playing"
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")


def get_color(imgURL):
    try:
        resp = requests.get(imgURL)
        img = BytesIO(resp.content)
        color_thief = ColorThief(img)
        cor = color_thief.get_color(quality=10)
        return f"{cor[0]}, {cor[1]}, {cor[2]}"
    except:  # noqa
        return "30, 30, 30"


def opacityUpdate(rgb):
    r, g, b = rgb.split(",")
    lumin = 0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b)

    opacity = 0.25 - (lumin / 255) * 0.22
    opacity = max(0.08, min(0.25, opacity))

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
        return {{"playing": False, "error": "token falhou"}}

    response = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200 or not response.content:
        return {"playing": False}

    track = response.json()

    if not track or not track.get("is_playing"):
        return {"playing": False}

    item = track["item"]

    return {
        "playing": True,
        "track": item["name"],
        "artist": item["artists"][0]["name"],
        "album_cover": item["album"]["images"][0]["url"],
        "track_url": f"https://open.spotify.com/track/{item['id']}",
        "progress": {
            "current": track["progress_ms"] // 1000,
            "total": item["duration_ms"] // 1000,
        },
        "color": opacityUpdate(get_color(item["album"]["images"][0]["url"])),
    }
