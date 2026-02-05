from config import DISCORD_BOT_TOKEN, DISCORD_ID
import requests

TOKEN = DISCORD_BOT_TOKEN


def get_discord():
    URL = f"https://discord.com/api/v10/users/{DISCORD_ID}"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}

    response = requests.get(URL, headers=headers)

    if response.status_code != 200:
        return {"error": "falhou", "username": "hash", "global_name": "hash", "avatar": None}

    data = response.json()

    userName = data["username"]
    globalName = data["global_name"]
    avatar = data["avatar"]

    link = (
        f"https://cdn.discordapp.com/avatars/{DISCORD_ID}/{avatar}.png"
        if avatar 
        else None
    )

    return {
        "username": userName,
        "global_name": globalName,
        "avatar": link
    }