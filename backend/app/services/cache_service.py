import time
from app.config import CACHE_TTL_SECONDS

_store: dict = {}   # { key: {"data": ..., "ts": float} }


def get(key: str):
    entry = _store.get(key)
    if entry and (time.time() - entry["ts"]) < CACHE_TTL_SECONDS:
        return entry["data"]
    return None


def set(key: str, data):
    _store[key] = {"data": data, "ts": time.time()}


def invalidate(key: str):
    _store.pop(key, None)


def cache_age_seconds(key: str) -> float | None:
    entry = _store.get(key)
    if entry:
        return time.time() - entry["ts"]
    return None
