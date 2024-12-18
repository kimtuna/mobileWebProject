# parking_app/urls.py

from django.urls import path
from .views import detect_cars

urlpatterns = [
    path('detect/', detect_cars, name='detect_cars'),
]
