import spotipy
import requests
from io import BytesIO
from spotipy import SpotifyOAuth
from colorthief import ColorThief
from config import SPOTIFY_CLIENT, SPOTIFY_SECRET, SPOTIFY_REDIRECT

SCOPE_READ = "user-read-currently-playing"


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
    
    return f"rgba({r}, {g}, {b}, {opacity})"


def get_spotify():
    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth(
            client_id=SPOTIFY_CLIENT,
            client_secret=SPOTIFY_SECRET,
            redirect_uri=SPOTIFY_REDIRECT,
            scope=SCOPE_READ,
        )
    )

    track = sp.current_user_playing_track()

    if not track:
        return {"playing": False}

    is_playing = track["is_playing"]

    if is_playing:
        trackName = track["item"]["name"]
        artistName = track["item"]["artists"][0]["name"]
        albumCover = track["item"]["album"]["images"][0]["url"]

        duration = track["item"]["duration_ms"] // 1000
        progress = track["progress_ms"] // 1000
        trackId = track["item"]["id"]

        link = f"https://open.spotify.com/track/{trackId}"

        rgb = get_color(albumCover)

        return {
            "playing": is_playing,
            "track": trackName,
            "artist": artistName,
            "album_cover": albumCover,
            "track_url": link,
            "progress": {"current": progress, "total": duration},
            "color": opacityUpdate(rgb)
        }
    else:
        return {"playing": is_playing}
