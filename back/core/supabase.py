from config import SUPABASE_KEY, SUPABASE_URL
from requests.exceptions import RequestException
from supabase import create_client

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")

supa = create_client(SUPABASE_URL, SUPABASE_KEY)


def _safe_execute(query):
    try:
        result = query.execute()
        return result
    except RequestException as e:
        print(f"ERROR SUPABASE REQUEST: {e}")
    except Exception as e:
        print(f"ERROR SUPABASE EXECUTE: {e}")
    return None


def get_visit():
    result = _safe_execute(supa.table("stats").select("visits").eq("id", 1))
    if result and getattr(result, "data", None):
        return result.data[0].get("visits")
    return None


def add_visit():
    visit = get_visit()

    if visit is None:
        return None

    result = _safe_execute(
        supa.table("stats").update({"visits": visit + 1}).eq("id", 1)
    )

    return visit + 1 if result else None


def get_music_history():
    result = _safe_execute(supa.table("music_history").select("*").eq("id", 1))
    if result and getattr(result, "data", None) and result.data[0].get("track"):
        return result.data[0]
    return None


def save_music_history(data):
    _safe_execute(supa.table("music_history").update(data).eq("id", 1))


def get_game_session():
    result = _safe_execute(supa.table("game_session").select("*").eq("id", 1))
    if result and getattr(result, "data", None) and result.data[0].get("gameName"):
        return result.data[0]
    return None


def save_game_session(data):
    _safe_execute(supa.table("game_session").update(data).eq("id", 1))


def clear_game_session():
    _safe_execute(
        supa.table("game_session")
        .update({"gameName": None, "startedAt": None})
        .eq("id", 1)
    )


def get_api_status():
    result = _safe_execute(supa.table("stats").select("api_enabled").eq("id", 1))
    if result and getattr(result, "data", None):
        return result.data[0].get("api_enabled", True)
    return True


def set_api_status(status: bool):
    _safe_execute(supa.table("stats").update({"api_enabled": status}).eq("id", 1))
