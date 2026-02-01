import json
from pathlib import Path


path = Path("data/stats.json")


def get_visit():
    if path.exists():
        with path.open("r") as f:
            data = json.load(f)
    else:
        data = {"visits": 0}

    data["visits"] = data.get("visits") + 1

    with path.open("w") as f:
        json.dump(data, f)

    return {"success": True, "visits": data["visits"]}


def set_status(status: bool):
    with path.open("r") as f:
        data = json.load(f)

    data["status"] = status

    with path.open("w") as f:
        json.dump(data, f)

    if status:
        return {"success": "api on"}
    else:
        return {"success": "api off"}

def get_OnoF():
    with path.open("r") as f:
        stt = json.load(f)["status"]

    return stt
