import requests
from config import DISCORD_BOT_TOKEN, DISCORD_ID
from requests.exceptions import RequestException

TOKEN = DISCORD_BOT_TOKEN


def get_discord():
    if not DISCORD_BOT_TOKEN or not DISCORD_ID:
        return {
            "error": "missing discord credentials",
            "username": "hash",
            "global_name": "hash",
            "avatar": None,
        }

    URL = f"https://discord.com/api/v10/users/{DISCORD_ID}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}

    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except RequestException as e:
        print(f"ERROR DISCORD REQUEST: {e}")
        return {
            "error": "request failed",
            "username": "hash",
            "global_name": "hash",
            "avatar": None,
        }
    except ValueError as e:
        print(f"ERROR DISCORD JSON: {e}")
        return {
            "error": "invalid response",
            "username": "hash",
            "global_name": "hash",
            "avatar": None,
        }

    userName = data.get("username", "hash")
    globalName = data.get("global_name", "hash")
    avatar = data.get("avatar")

    link = (
        f"https://cdn.discordapp.com/avatars/{DISCORD_ID}/{avatar}.png"
        if avatar
        else None
    )

    return {"username": userName, "global_name": globalName, "avatar": link}
