import time

METRICS = []

def log_metric(data):
    METRICS.append({
        "timestamp": time.time(),
        **data
    })

def get_metrics():
    return METRICS