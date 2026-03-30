# core/middleware/load_shedding.py

from django.http import JsonResponse

from core.utils.rate_tracker import track_request
from core.utils.queue_tracker import (
    increment_queue,
    decrement_queue,
    get_queue_length
)
from core.utils.retry_tracker import is_retry
from core.services.priority import get_priority
from core.services.scoring import score_request
from core.services.degradation import degrade_response
from core.tasks import log_metrics_task
from core.utils.prometheus_metrics import (
    REQUEST_COUNT,
    QUEUE_LENGTH,
    USER_RATE
)


class LoadSheddingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        increment_queue()

        try:
            return self.handle_request(request)

        finally:
            decrement_queue()

   
    def handle_request(self, request):

        #  Identify user
        user_key = self.get_user_key(request)

        #  Track per-user rate
        user_rate = track_request(user_key)

        #  Detect retries 
        if is_retry(request):
            return JsonResponse(
                {"error": "Too many retries"},
                status=429,
                headers={"Retry-After": "5"}
            )

        # Get current system load
        queue_length = get_queue_length()

        # Assign priority
        priority = get_priority(request)

        #  ML / rule-based scoring
        decision = score_request({
            "user_rate": user_rate,
            "queue_length": queue_length,
            "priority_score": priority["priority_score"],
            "user_type": priority["user_type"],
            "request_type": priority["request_type"],
            "path": request.path,
            "method": request.method
        })

        # metrics log
        log_metrics_task.delay({
            "user_rate": user_rate,
            "queue_length": queue_length,
            "priority_score": priority["priority_score"],
            "decision": decision,
            "path": request.path
        })

        QUEUE_LENGTH.set(queue_length)
        USER_RATE.set(user_rate)
        REQUEST_COUNT.labels(decision=decision).inc()

        # Decision engine
        if decision == "DROP":
            return JsonResponse(
                {"error": "Request dropped due to overload"},
                status=503
            )

        elif decision == "DEGRADE":
            return degrade_response(request)

        
        response = self.get_response(request)
        return response

    #  User identity 
    def get_user_key(self, request):
        if hasattr(request, "user") and request.user.is_authenticated:
            return f"user_{request.user.id}"

        
        return request.META.get("REMOTE_ADDR", "anonymous")