from config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

supa = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_visit():
    result = supa.table("stats").select("visits").eq("id", 1).execute()
    if result.data:
        return result.data[0]["visits"]
    return 0


def add_visit():
    visit = get_visit()
    supa.table("stats").update({"visits": visit + 1}).eq("id", 1).execute()
    return visit + 1


def get_music_history():
    result = supa.table("music_history").select("*").eq("id", 1).execute()
    if result.data and result.data[0]["track"]:
        return result.data[0]
    return None


def save_music_history(data):
    supa.table("music_history").update(data).eq("id", 1).execute()


def get_game_session():
    result = supa.table("game_session").select("*").eq("id", 1).execute()
    if result.data and result.data[0]["gameName"]:
        return result.data[0]
    return None


def save_game_session(data):
    supa.table("game_session").update(data).eq("id", 1).execute()


def clear_game_session():
    supa.table("game_session").update({"gameName": None, "startedAt": None}).eq(
        "id", 1
    ).execute()


def get_api_status():
    result = supa.table("stats").select("api_enabled").eq("id", 1).execute()
    if result.data:
        return result.data[0]["api_enabled"]
    return True

def set_api_status(status: bool):
    supa.table("stats").update({"api_enabled": status}).eq("id", 1).execute()