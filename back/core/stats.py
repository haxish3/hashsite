from .supabase import get_api_status, set_api_status, get_visit, add_visit


def get_visits():
    add_visit()
    return {"success": True, "visits": get_visit()}


def set_status(status: bool):
    set_api_status(status)
    return {"msg": f"success: api {'online' if status else 'offline'}"}


def get_OnoF():
    return get_api_status()
