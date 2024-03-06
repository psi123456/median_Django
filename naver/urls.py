# naver/urls.py

from django.urls import path
from .views import search_pharmacies

urlpatterns = [
    path('search/', search_pharmacies, name='search_pharmacies'),
]
