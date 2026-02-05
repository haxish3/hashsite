import json
from pathlib import Path


path = Path("data/stats.json")


def get_visit():
    if path.exists():
        with path.open("r") as f:
            data = json.load(f)
    else:
        data = {"visits": 0}

    data["visits"] = (data.get("visits") + 1) if data.get("visits") else 1

    with path.open("w") as f:
        json.dump(data, f)

    return {"success": True, "visits": data["visits"]}


def set_status(status: bool):
    if path.exists():
        with path.open("r") as f:
            data = json.load(f)
    else:
        data = {"api_enabled": status}

    data["api_enabled"] = status

    with path.open("w") as f:
        json.dump(data, f, indent=4)

    return {"msg": f"success: api {'online' if status else 'offline'}"}


def get_OnoF():
    if path.exists():
        with path.open("r") as f:
            try:
                stt = json.load(f)["api_enabled"]
            except Exception as e:
                return True
                print(f"ERROR: 'get_OnoF': {e}")

        return stt
    return True
