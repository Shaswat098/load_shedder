from django.urls import path
from . import views

urlpatterns = [
    path('recommend', views.recommendation_view),
    path('search/',views.search_view),
    path('metrics/', views.metrics_view),
]