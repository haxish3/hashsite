import os
from dotenv import load_dotenv

load_dotenv()

ROBLOX_COOKIE = os.getenv("ROBLOX_COOKIE")
ROBLOX_USER_ID = os.getenv("ROBLOX_USER_ID")
ROBLOX_API = "https://presence.roblox.com/v1/presence/users"

SPOTIFY_CLIENT = os.getenv("SPOTIFY_CLIENT")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
SPOTIFY_REDIRECT = os.getenv("SPOTIFY_REDIRECT", "http://127.0.0.1:8888/callback")

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_ID = os.getenv("DISCORD_ID")
DISCORD_API = "https://discord.com/api/v10/users/{user_id}"