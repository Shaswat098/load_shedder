from collections import defaultdict, deque
import time
import hashlib

retry_store = defaultdict(deque)

RETRY_WINDOW = 10 #seconds
MAX_RETRIES = 3

def get_request_fingerprint(request):
    user = request.user.id if hasattr(request,"user") and request.user.is_authenticated else "anon"
    path = request.path
    method = request.method

    query = request.META.get("QUERY_STRING","")
    raw = f"{user}:{method}:{path}:{query}"

    return hashlib.md5(raw.encode()).hexdigest()


def is_retry(request):
    now = time.time()

    fingerprint = get_request_fingerprint(request)
    dq = retry_store[fingerprint]

    dq.append(now)

    # Remove old entries
    while dq and now - dq[0] > RETRY_WINDOW:
        dq.popleft()

    if len(dq) > MAX_RETRIES:
        return True
    
    return False