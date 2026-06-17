"""
storage.py — tiny, dependency-free cross-platform key/value persistence.

Priority order (first that works wins):
  1. Browser localStorage   — when running under Pygbag/WASM in a browser
  2. JSON file on disk       — desktop (`python main.py`)
  3. In-memory dict          — last-resort fallback so the game never crashes

Everything is wrapped in broad try/except: persistence is a nice-to-have, never
allowed to take the game down (especially important inside the WASM sandbox).
"""
import json

_KEY  = "kesra_save"
_FILE = "kesra_save.json"
_MEM: dict[str, str] = {}


def _local_storage():
    """Return the browser localStorage object under Pygbag, else None."""
    try:
        import platform
        return platform.window.localStorage
    except Exception:
        return None


def save(data: dict) -> None:
    blob = json.dumps(data)

    ls = _local_storage()
    if ls is not None:
        try:
            ls.setItem(_KEY, blob)
            return
        except Exception:
            pass

    try:
        with open(_FILE, "w", encoding="utf-8") as f:
            f.write(blob)
        return
    except Exception:
        pass

    _MEM[_KEY] = blob


def load() -> dict:
    ls = _local_storage()
    if ls is not None:
        try:
            blob = ls.getItem(_KEY)
            if blob:
                return json.loads(blob)
        except Exception:
            pass

    try:
        with open(_FILE, encoding="utf-8") as f:
            return json.loads(f.read())
    except Exception:
        pass

    blob = _MEM.get(_KEY)
    if blob:
        try:
            return json.loads(blob)
        except Exception:
            pass
    return {}
