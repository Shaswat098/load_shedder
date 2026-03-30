from collections import deque, defaultdict
import time

WINDOW_SIZE = 60 #seconds

user_requests = defaultdict(deque)

def track_request(user_key):
    now = time.time()
    dq = user_requests[user_key]

    dq.append(now)

    # Remove old requests outside window
    while dq and now - dq[0] > WINDOW_SIZE:
        dq.popleft()

    return len(dq) # requests in last 60 sec for THIS user