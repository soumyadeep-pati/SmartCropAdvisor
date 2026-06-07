from django.urls import path
from .views import weather_history, weather_view

urlpatterns = [
    path('', weather_view, name='weather'),
    path('history/', weather_history, name='weather_history'),
]
