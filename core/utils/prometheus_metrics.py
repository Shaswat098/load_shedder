from prometheus_client import Counter, Gauge

REQUEST_COUNT = Counter(
    'requests_total',
    'Total_requests',
    ['decision']
)

QUEUE_LENGTH = Gauge(
    'queue_length',
    'Current queue size'
)

USER_RATE = Gauge(
    'user_rate',
    "Requets per user"
)