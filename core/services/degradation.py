from django.http import JsonResponse

from core.utils.cache_store import get_cache

def degrade_response(request):

    path = request.path.lower()
    
    # For recommendations
    if "recommend" in path:

        data = get_cache("recommendations") or []
        return JsonResponse({
            "data": data,
            "degraded": True,
            "source": "cache",
            "message": "Showing limited results due to high load"
        })
    
    # For APIs
    elif "search" in path:

        query = request.GET.get("q","")
        cache_key = f"search_{query}"
        data = get_cache(cache_key) or []
        return JsonResponse({
            "data":data,
            "degraded":True,
            "source":"cache",
            "message": "Search temporarily limited, try again later"
        })
    
    # For payment

    elif "payment" in path or "checkout" in path:
        return JsonResponse({
            "error": "Server busy, please retry"
        },status = 503)
    
    # Default
    return JsonResponse({
        "message" : "Service running in degraded mode",
        "degraded":True
    })
        