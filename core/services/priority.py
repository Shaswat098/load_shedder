
USER_WEIGHTS = {
    "premium" : 3,
    "normal" : 2,
    "anonymous" : 1
}

REQUEST_WEIGHTS = {
    "payment" : 5,
    "search" : 3,
    "recommendation" : 1,
    "default" : 2
}

def get_request_type(request):
    path = request.path.lower()

    if "payment" in path or "checkout" in path:
        return "payment"
    elif "search" in path:
        return "search"
    elif "recommend" in path:
        return "recommendation"
    else:
        return "default"
    
def get_user_type(request):
    if hasattr(request,"user") and request.user.is_authenticated:
        return getattr(request.user, "account_type", "normal")
    return "anonymous"


def get_priority(request):
    
    user_type = get_user_type(request)
    request_type = get_request_type(request)

    user_score = USER_WEIGHTS.get(user_type, 1)
    request_score = REQUEST_WEIGHTS.get(request_type, 2)

    priority = user_score + request_score

    return {
        "priority_score" : priority,
        "user_type" : user_type,
        "request_type" : request_type
    }