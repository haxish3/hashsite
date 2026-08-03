import base64
import os
from datetime import datetime, timezone
from io import BytesIO

import requests
from colorthief import ColorThief
from config import SPOTIFY_CLIENT, SPOTIFY_SECRET
from requests.exceptions import RequestException

from .supabase import get_music_history, save_music_history

REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")


def get_color(imgURL):
    if not imgURL:
        return "30, 30, 30"

    try:
        resp = requests.get(imgURL, timeout=10)
        resp.raise_for_status()
        img = BytesIO(resp.content)
        color_thief = ColorThief(img)
        cor = color_thief.get_color(quality=10)
        return f"{cor[0]}, {cor[1]}, {cor[2]}"
    except RequestException as e:
        print(f"ERROR SPOT COLOR REQUEST: {e}")
    except Exception as e:
        print(f"ERROR SPOT COLOR: {e}")

    return "30, 30, 30"


def opacityUpdate(rgb):
    try:
        r, g, b = rgb.split(",")
        lumin = 0.299 * int(r) + 0.587 * int(g) + 0.114 * int(b)

        opc = 0.25
        opacity = opc - (lumin / 255) * 0.22
        opacity = max(0.08, min(opc, opacity))

        return f"rgba({r}, {g}, {b}, {opacity:.2f})"
    except Exception as e:
        print(f"ERROR SPOT OPACITY: {e}")
        return "rgba(30, 30, 30, 0.08)"


def get_access_token():
    if not SPOTIFY_CLIENT or not SPOTIFY_SECRET or not REFRESH_TOKEN:
        print("ERROR SPOTIFY: missing credentials or refresh token")
        return None

    auth = base64.b64encode(f"{SPOTIFY_CLIENT}:{SPOTIFY_SECRET}".encode()).decode()

    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "refresh_token", "refresh_token": REFRESH_TOKEN},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except RequestException as e:
        print(f"ERROR SPOTIFY TOKEN REQUEST: {e}")
        return None
    except ValueError as e:
        print(f"ERROR SPOTIFY TOKEN DECODE: {e}")
        return None

    if "access_token" not in data:
        print(f"ERRO SPOTIFY: {data}")
        return None

    return data["access_token"]


def get_spotify():
    token = get_access_token()

    if not token:
        return {"playing": False, "error": "token failure"}

    try:
        response = requests.get(
            "https://api.spotify.com/v1/me/player/currently-playing",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        if response.status_code == 204 or not response.content:
            track = {"is_playing": False}
        else:
            response.raise_for_status()
            track = response.json()
    except RequestException as e:
        print(f"ERROR SPOTIFY PLAYER REQUEST: {e}")
        track = {"is_playing": False}
    except ValueError as e:
        print(f"ERROR SPOTIFY PLAYER DECODE: {e}")
        track = {"is_playing": False}

    is_playing = bool(track.get("is_playing"))
    item = track.get("item")

    if is_playing and item:
        try:
            save_music_history(
                {
                    "track": item.get("name"),
                    "artist": item.get("artists", [{}])[0].get("name"),
                    "album_cover": item.get("album", {})
                    .get("images", [{}])[0]
                    .get("url"),
                    "track_url": item.get("external_urls", {}).get("spotify"),
                }
            )
            history_saved = True
        except Exception as e:
            history_saved = False
            print(f"ERROR SPOT: DONT SAVED HISTORY --- {e}")

        return {
            "playing": True,
            "history_saved": history_saved,
            "track": item.get("name"),
            "artist": item.get("artists", [{}])[0].get("name"),
            "album_cover": item.get("album", {}).get("images", [{}])[0].get("url"),
            "track_url": item.get("external_urls", {}).get("spotify"),
            "progress": {
                "current": track.get("progress_ms", 0) // 1000,
                "total": item.get("duration_ms", 0) // 1000,
            },
            "color": opacityUpdate(
                get_color(item.get("album", {}).get("images", [{}])[0].get("url"))
            ),
        }

    history = get_music_history()
    if history:
        try:
            updated_at = datetime.fromisoformat(
                history.get("updated_at", "").replace("+00", "+00:00")
            )
            now = datetime.now(timezone.utc)
            sec = int((now - updated_at).total_seconds())
        except Exception as e:
            print(f"ERROR SPOT HISTORY PARSE: {e}")
            sec = 0

        return {
            "playing": False,
            "has_history": True,
            "track": history.get("track"),
            "artist": history.get("artist"),
            "album_cover": history.get("album_cover"),
            "track_url": history.get("track_url"),
            "color": "rgba(0, 0, 0, 0)",
            "elapsed": sec,
        }

    return {"playing": False, "has_history": False}
