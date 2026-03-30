import time

CACHE = {}
CACHE_TTL = 60 #seconds

def set_cache(key, data):
    CACHE[key] = {
        "data": data,
        "timestamp": time.time()
    }

def get_cache(key):
    entry = CACHE.get(key)
    if not entry:
        return None
    
    if time.time() - entry["timestamp"] > CACHE_TTL:
        del CACHE[key]
        return None
    
    return entry["data"]