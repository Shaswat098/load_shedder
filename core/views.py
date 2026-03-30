from core.tasks import update_cache_task
from core.utils.cache_store import set_cache
from django.http import JsonResponse,HttpResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

def recommendation_view(request):

    data = [
        {"id":1, "name": "Laptop"},
        {"id":2, "name": "Phone"}
    ]

    if data:
        update_cache_task.delay("recommendations", data)

    return JsonResponse({
        "data": data,
        "source": "live"
    })

def search_view(request):
    query = request.GET.get("q", "")

    data = [
        {"id":101, "title":f"Result for {query}"}
    ]

    cache_key = f"search_{query}"

    if data:
        update_cache_task.delay(cache_key,data)

    return JsonResponse({
        "data": data,
        "source": "live"
    })

def metrics_view(request):
    return HttpResponse(generate_latest(), content_type = CONTENT_TYPE_LATEST)