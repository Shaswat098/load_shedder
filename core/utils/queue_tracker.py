import threading

# General queue counter
current_requests = 0
lock = threading.Lock()

def increment_queue():
    global current_requests
    with lock:
        current_requests += 1

def decrement_queue():
    global current_requests
    with lock:
        current_requests -= 1

def get_queue_length():
    return current_requests